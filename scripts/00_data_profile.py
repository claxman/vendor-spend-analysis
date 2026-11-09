#!/usr/bin/env python3
"""Profile the raw vendor spend workbook and write a Markdown data profile.

Read-only by construction: the workbook is loaded from a binary file handle and
never saved. The source file's SHA-256 is recorded in the output so a later run
can prove the raw file was not modified.

Usage:
    python scripts/00_data_profile.py [xlsx_path] [output_md_path]
Defaults:
    data/raw/vendor_analysis_assessment.xlsx -> outputs/analysis/00_data_profile.md
"""
from __future__ import annotations

import hashlib
import re
import sys
import unicodedata
from collections import Counter, defaultdict
from datetime import date, datetime
from difflib import SequenceMatcher
from pathlib import Path

from openpyxl import load_workbook
from openpyxl.utils import get_column_letter

RAW_DEFAULT = Path("data/raw/vendor_analysis_assessment.xlsx")
OUT_DEFAULT = Path("outputs/analysis/00_data_profile.md")
TAXONOMY_PATH = Path("docs/taxonomy.md")
MAIN_SHEET = "Vendor Analysis Assessment"
CONFIG_SHEET = "Config"
NAME_COL, DEPT_COL, COST_COL, DESC_COL, SUGG_COL = 0, 1, 2, 3, 4
SMALL_VENDOR_THRESHOLD = 1000.0
FUZZY_RATIO = 0.85
MAX_LIST_ROWS = 60
EM_DASH = "\u2014"

# Tokens removed before comparing vendor names. Legal forms and geography do
# not identify a vendor: "Acme Ltd" and "Acme Inc" are one vendor family for
# consolidation purposes even if they are separate legal entities.
LEGAL_TOKENS = {
    "ltd", "limited", "llc", "inc", "incorporated", "corp", "corporation",
    "co", "company", "plc", "gmbh", "ag", "sa", "sas", "sarl", "srl", "bv",
    "bvba", "nv", "doo", "jdoo", "dd", "sro", "sl", "pc", "pp", "vl", "obrt",
    "pvt", "private", "pte", "pty", "llp", "lp", "kft", "oy", "ab", "as",
    "aps", "ltda", "spa", "kk", "spzoo",
}
GEO_TOKENS = {
    "uk", "usa", "us", "gb", "eu", "ireland", "india", "europe", "emea",
    "america", "amer", "international", "intl", "global", "croatia",
    "hrvatska", "australia", "australian", "aus", "singapore", "sg", "nsw",
    "wa", "victoria", "london", "zagreb", "split", "melbourne", "chennai",
    "greece", "greec",
}
STOP_TOKENS = {"the", "and", "of", "a", "za", "i", "u"}
NOISE_TOKENS = {"supplier", "com"}
CROATIAN_FORM_TOKENS = {"doo", "jdoo", "dd", "obrt"}
PLACEHOLDER_NAMES = {"(blank)", "blank", "n/a", "na", "none", "unknown", "null", "-", "tbd"}

CURRENCY_PATTERN = re.compile(
    r"[$\u20ac\u00a3\u00a5\u20b9]|\b(usd|eur|gbp|inr|hrk|chf|cad|aud|jpy|sgd)\b",
    re.IGNORECASE,
)

# Manual observations used only in the proposal text. The script cites a name
# only if it is actually present in the data (raw or repaired form).
OBSERVED_PERSON_NAMES = [
    "Ansar Madovic", "Fabiola Thistlewhaite", "George Anchor", "John Smith",
    "Stipe Piric", "Susan Lee",
]
OBSERVED_STATUTORY = [
    "Australian Taxation Office (Ato)", "Cayman Islands Government", "Grad Split",
    "Grad Zagreb, Gradski Ured Za Prostorno Ure\u0111enje,..", "Icare Nsw", "Ico",
]
OBSERVED_CARD_MERCHANTS = [
    "Coles", "M&S Simply Food", "Pret A Manger", "Uber *Eats", "Officeworks",
    "Currys Pc World", "Snappy Snaps", "Post Office Ltd",
]


# ---------------------------------------------------------------- helpers

def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def is_blank(v) -> bool:
    return v is None or (isinstance(v, str) and v.strip() == "")


def type_name(v) -> str:
    if is_blank(v):
        return "blank"
    if isinstance(v, bool):
        return "bool"
    if isinstance(v, int):
        return "int"
    if isinstance(v, float):
        return "float"
    if isinstance(v, datetime):
        return "datetime"
    if isinstance(v, str):
        return "str"
    return type(v).__name__


def is_number(v) -> bool:
    return isinstance(v, (int, float)) and not isinstance(v, bool)


def money(x: float) -> str:
    sign = "-" if x < 0 else ""
    return f"{sign}${abs(x):,.0f}"


def pct(x: float) -> str:
    return f"{100 * x:.1f}%"


def md_escape(s) -> str:
    return str(s).replace("|", "\\|").replace("\n", " ")


def table(headers: list[str], rows: list[list]) -> list[str]:
    out = ["| " + " | ".join(headers) + " |", "|" + "|".join(["---"] * len(headers)) + "|"]
    for r in rows:
        out.append("| " + " | ".join(md_escape(c) for c in r) + " |")
    return out


def decimals_of(x: float) -> int:
    if isinstance(x, int) or float(x).is_integer():
        return 0
    text = repr(float(x))
    if "e" in text or "E" in text:
        return 15
    return len(text.split(".")[1])


# ---------------------------------------------------------------- text repair

LEAD_FIX = {"\u00e3": "\u00c3", "\u00e4": "\u00c4", "\u00e5": "\u00c5"}  # a-tilde, a-umlaut, a-ring
CASE_FLIP = {"\u0161": "\u0160", "\u0153": "\u0152", "\u017e": "\u017d"}  # s-caron, oe, z-caron
MOJIBAKE_MARKER = re.compile(r"[\u00c0-\u00c5\u00e0-\u00e5\u0080-\u009f]|_x00[0-9a-f]{2}_", re.IGNORECASE)
EXCEL_ESCAPE = re.compile(r"_x([0-9A-Fa-f]{4})_")


def _cp1252_bytes(t: str) -> bytes:
    out = bytearray()
    for ch in t:
        o = ord(ch)
        if 0x80 <= o <= 0x9F:  # undefined cp1252 slots survive as raw bytes
            out.append(o)
        else:
            out += ch.encode("cp1252")
    return bytes(out)


def repair_mojibake(s: str) -> tuple[str, bool]:
    """Undo UTF-8 text that was decoded as cp1252 and then Title Cased.

    Title casing turned lead bytes C3/C4/C5 into lower-case a-tilde/a-umlaut/
    a-ring when they fell mid-word, so those are restored before re-encoding.
    Excel's _x008d_ escapes stand for bytes cp1252 cannot show.
    """
    if not MOJIBAKE_MARKER.search(s):
        return s, False
    base = EXCEL_ESCAPE.sub(lambda m: chr(int(m.group(1), 16)), s)
    v2 = "".join(LEAD_FIX.get(ch, ch) for ch in base)
    variants = [
        base,
        v2,
        "".join(CASE_FLIP.get(ch, ch) for ch in v2),
        v2.replace("\u00c5 ", "\u00c5\u00a0"),
    ]
    for v in variants:
        try:
            fixed = _cp1252_bytes(v).decode("utf-8")
        except (UnicodeEncodeError, UnicodeDecodeError):
            continue
        if fixed != s:
            fixed = re.sub(r"(?<=[^\W\d_])([^\W\d_])", lambda m: m.group(1).lower(), fixed)
            return fixed, True
    return s, False


TRANSLIT = {"\u0111": "d", "\u0110": "D", "\u00df": "ss", "\u0142": "l", "\u0141": "L",
            "\u00f8": "o", "\u00d8": "O", "\u00e6": "ae", "\u00c6": "AE"}


def strip_accents(s: str) -> str:
    s = "".join(TRANSLIT.get(ch, ch) for ch in s)
    return "".join(ch for ch in unicodedata.normalize("NFKD", s) if not unicodedata.combining(ch))


def normalize_name(name: str) -> str:
    s = strip_accents(repair_mojibake(name)[0]).lower()
    s = s.replace("&", " and ")
    s = re.sub(r"\ba/s\b", " as ", s)
    s = re.sub(r"\b((?:[a-z]\.){2,})", lambda m: m.group(1).replace(".", ""), s)  # d.o.o. -> doo
    s = re.sub(r"\bsp\.?\s*z\s*o\.?\s*o\b\.?", " spzoo ", s)
    s = re.sub(r"[^a-z0-9 ]+", " ", s)
    drop = LEGAL_TOKENS | GEO_TOKENS | STOP_TOKENS | NOISE_TOKENS
    return " ".join(t for t in s.split() if t not in drop)


# ---------------------------------------------------------------- generic sheet profile

def last_data_row(ws) -> int:
    last = 0
    for row in ws.iter_rows(min_row=1, max_row=ws.max_row):
        if any(not is_blank(c.value) for c in row):
            last = row[0].row
    return last


def profile_sheet(ws, ws_formulas) -> dict:
    """Column-level profile of any sheet, treating row 1 as the header."""
    last = last_data_row(ws)
    header = [c.value for c in next(ws.iter_rows(min_row=1, max_row=1))]
    cols = []
    for idx in range(ws.max_column):
        letter = get_column_letter(idx + 1)
        head = header[idx] if idx < len(header) else None
        types: Counter = Counter()
        formats: Counter = Counter()
        for row in ws.iter_rows(min_row=2, max_row=max(last, 2), min_col=idx + 1, max_col=idx + 1):
            c = row[0]
            types[type_name(c.value)] += 1
            if not is_blank(c.value):
                formats[c.number_format] += 1
        data_rows = max(last - 1, 0)
        blanks = types.get("blank", 0) if data_rows else 0
        cols.append({
            "letter": letter,
            "header": "(no header)" if is_blank(head) else str(head),
            "non_blank": data_rows - blanks,
            "blank": blanks,
            "types": {k: v for k, v in types.items() if k != "blank"},
            "formats": formats,
        })
    rows_with_values = sum(
        1 for row in ws.iter_rows(min_row=1, max_row=ws.max_row)
        if any(not is_blank(c.value) for c in row)
    )
    formula_cells = sum(
        1 for row in ws_formulas.iter_rows(min_row=1, max_row=ws_formulas.max_row)
        for c in row if isinstance(c.value, str) and c.value.startswith("=")
    )
    validations = []
    for dv in ws.data_validations.dataValidation:
        validations.append(f"{dv.sqref}: type={dv.type}, formula={dv.formula1}")
    return {
        "title": ws.title,
        "dims": ws.dimensions,
        "max_row": ws.max_row,
        "max_col": ws.max_column,
        "state": ws.sheet_state,
        "last_data_row": last,
        "rows_with_values": rows_with_values,
        "data_rows": max(last - 1, 0),
        "trailing_blank_rows": ws.max_row - last,
        "formula_cells": formula_cells,
        "validations": validations,
        "columns": cols,
        "cells": [
            (c.coordinate, c.value)
            for row in ws.iter_rows(min_row=1, max_row=max(last, 1))
            for c in row if not is_blank(c.value)
        ],
    }


def render_sheet_profile(p: dict) -> list[str]:
    out = [
        f"Used range `{p['dims']}`: {p['max_row']} rows x {p['max_col']} columns, sheet state `{p['state']}`. "
        f"Rows with any value: {p['rows_with_values']}. Header row: 1. "
        f"Data rows (2 to {p['last_data_row']}): {p['data_rows']}. "
        f"Trailing blank rows inside the used range: {p['trailing_blank_rows']}. "
        f"Formula cells: {p['formula_cells']}. "
        + ("Data validation: " + "; ".join(p["validations"]) + "." if p["validations"] else "Data validation: none."),
        "",
    ]
    rows = []
    for c in p["columns"]:
        types = ", ".join(f"{k}: {v}" for k, v in sorted(c["types"].items())) or "(none)"
        fmts = ", ".join(f"`{k}`: {v}" for k, v in c["formats"].most_common(3)) or "(none)"
        rows.append([c["letter"], c["header"], c["non_blank"], c["blank"], types, fmts])
    out += table(["Col", "Header", "Non-blank", "Blank", "Value types (count)", "Number formats (count)"], rows)
    return out


# ---------------------------------------------------------------- main sheet analysis

def load_vendor_rows(ws, last: int) -> list[dict]:
    rows = []
    for row in ws.iter_rows(min_row=2, max_row=last):
        vals = [c.value for c in row]
        rec = {
            "row": row[0].row,
            "name": vals[NAME_COL] if len(vals) > NAME_COL else None,
            "dept": vals[DEPT_COL] if len(vals) > DEPT_COL else None,
            "cost": vals[COST_COL] if len(vals) > COST_COL else None,
            "desc": vals[DESC_COL] if len(vals) > DESC_COL else None,
            "sugg": vals[SUGG_COL] if len(vals) > SUGG_COL else None,
            "cost_format": row[COST_COL].number_format if len(row) > COST_COL else None,
        }
        if any(not is_blank(v) for v in vals):
            rows.append(rec)
    return rows


def group_label(recs: list[dict]) -> str:
    return "; ".join(
        f"`{r['name']}` (row {r['row']}, {money(float(r['cost'])) if is_number(r['cost']) else 'cost n/a'})"
        for r in recs
    )


def group_total(recs: list[dict]) -> float:
    return sum(float(r["cost"]) for r in recs if is_number(r["cost"]))


def analyze_main(ws, p: dict) -> dict:
    recs = load_vendor_rows(ws, p["last_data_row"])
    named = [r for r in recs if not is_blank(r["name"])]
    unnamed = [r for r in recs if is_blank(r["name"])]
    numeric = [r for r in named if is_number(r["cost"])]
    non_numeric_cost = [r for r in named if not is_number(r["cost"])]
    names = [str(r["name"]) for r in named]

    repairs = []
    for r in named:
        fixed, changed = repair_mojibake(str(r["name"]))
        r["name_fixed"] = fixed
        if changed:
            repairs.append((r["row"], str(r["name"]), fixed, float(r["cost"]) if is_number(r["cost"]) else 0.0))
    still_marked = [str(r["name"]) for r in named
                    if r["name_fixed"] == r["name"] and MOJIBAKE_MARKER.search(str(r["name"]))]
    names_all = set(names) | {r["name_fixed"] for r in named}

    hygiene = {
        "lead_trail_space": [n for n in names if n != n.strip()],
        "double_space": [n for n in names if "  " in n],
        "all_caps": [n for n in names if n.isupper() and any(ch.isalpha() for ch in n)],
        "all_lower": [n for n in names if n.islower()],
        "title_case_share": sum(1 for n in names if n == n.title()) / len(names) if names else 0.0,
        "has_digit": [r["name_fixed"] for r in named if any(ch.isdigit() for ch in r["name_fixed"])],
        "short": [n for n in names if len(n.strip()) < 3],
        "non_ascii": [n for n in names if any(ord(ch) > 127 for ch in n)],
        "excel_escape": [n for n in names if EXCEL_ESCAPE.search(n)],
        "em_dash": [n for n in names if EM_DASH in n],
        "parenthetical": [n for n in names if "(" in n],
        "dash_alias": [n for n in names if " - " in n],
        "trailing_suffix": [n for n in names
                            if re.search(r"\b(ltd|limited|inc|llc|gmbh|doo|plc|llp)-[A-Za-z]{2,5}$", n.strip(), re.IGNORECASE)],
        "trailing_ellipsis": [n for n in names if n.strip().endswith("..")],
        "placeholder": [n for n in names if n.strip().lower() in PLACEHOLDER_NAMES],
        "supplier_tag": [n for n in names if re.search(r"\bsupplier\b", n, re.IGNORECASE)],
        "card_descriptor": [n for n in names if "*" in n],
        "max_len": max((len(n) for n in names), default=0),
    }
    hygiene["at_max_len"] = [n for n in names if len(n) == hygiene["max_len"]]
    placeholder_recs = [r for r in named if str(r["name"]).strip().lower() in PLACEHOLDER_NAMES]

    exact: dict[str, list[dict]] = defaultdict(list)
    for r in named:
        exact[str(r["name"])].append(r)
    exact_dups = {k: v for k, v in exact.items() if len(v) > 1}

    casefold: dict[str, list[dict]] = defaultdict(list)
    for r in named:
        casefold[" ".join(str(r["name"]).lower().split())].append(r)
    casefold_dups = {k: v for k, v in casefold.items()
                     if len(v) > 1 and len({str(x["name"]) for x in v}) > 1}

    norm: dict[str, list[dict]] = defaultdict(list)
    for r in named:
        r["key"] = normalize_name(str(r["name"]))
        norm[r["key"]].append(r)
    norm_dups = {k: v for k, v in norm.items()
                 if k and len(v) > 1 and len({str(x["name"]) for x in v}) > 1}
    empty_key = norm.get("", [])

    keys = sorted(k for k in norm if k)
    tokens = {k: set(k.split()) for k in keys}
    near, flagged_pairs = [], set()
    for i, a in enumerate(keys):
        ta = tokens[a]
        for b in keys[i + 1:]:
            tb = tokens[b]
            shared = ta & tb
            smaller = min(len(ta), len(tb))
            subset = (ta <= tb or tb <= ta) and min(len(a), len(b)) >= 3
            shared_tokens = len(shared) >= 2 and len(shared) / smaller >= 0.5
            sm = SequenceMatcher(None, a, b)
            similar = (sm.real_quick_ratio() >= FUZZY_RATIO and sm.quick_ratio() >= FUZZY_RATIO
                       and sm.ratio() >= FUZZY_RATIO)
            if similar:
                rule = "similar spelling"
            elif subset:
                rule = "token subset"
            elif shared_tokens:
                rule = "shared tokens"
            else:
                continue
            near.append({"a": a, "b": b, "ratio": sm.ratio(), "rule": rule})
            flagged_pairs.add(frozenset((a, b)))
    near.sort(key=lambda d: (-(group_total(norm[d["a"]]) + group_total(norm[d["b"]]))))

    first: dict[str, set[str]] = defaultdict(set)
    for k in keys:
        t = k.split()[0]
        if len(t) >= 2:
            first[t].add(k)
    weak = {}
    for t, ks in first.items():
        if len(ks) < 2:
            continue
        ks_sorted = sorted(ks)
        unflagged = any(frozenset((x, y)) not in flagged_pairs
                        for i, x in enumerate(ks_sorted) for y in ks_sorted[i + 1:])
        if unflagged:
            weak[t] = ks_sorted
    weak_sorted = sorted(weak.items(), key=lambda kv: -sum(group_total(norm[k]) for k in kv[1]))

    cost_formats = Counter(r["cost_format"] for r in numeric)
    fractional = [r for r in numeric if not float(r["cost"]).is_integer()]
    max_decimals = max((decimals_of(r["cost"]) for r in numeric), default=0)
    entity_tokens: Counter = Counter()
    croatian_rows = 0
    for r in named:
        s = strip_accents(r["name_fixed"]).lower()
        s = re.sub(r"\b((?:[a-z]\.){2,})", lambda m: m.group(1).replace(".", ""), s)
        toks = set(re.sub(r"[^a-z0-9 ]+", " ", s).split())
        hits = toks & (LEGAL_TOKENS | GEO_TOKENS)
        for t in hits:
            entity_tokens[t] += 1
        if toks & CROATIAN_FORM_TOKENS:
            croatian_rows += 1
    text_currency_hits, raw_only_hits = [], []
    for r in recs:
        for key in ("name", "dept", "desc", "sugg"):
            v = r.get("name_fixed", r["name"]) if key == "name" else r[key]
            if isinstance(v, str) and CURRENCY_PATTERN.search(v):
                text_currency_hits.append((r["row"], key, v))
            elif key == "name" and isinstance(r["name"], str) and CURRENCY_PATTERN.search(r["name"]):
                raw_only_hits.append((r["row"], r["name"]))

    costs = sorted((float(r["cost"]) for r in numeric), reverse=True)
    total = sum(costs)
    n = len(costs)
    ranked = sorted(numeric, key=lambda r: float(r["cost"]), reverse=True)
    by_row = sorted(numeric, key=lambda r: r["row"])
    inversions = [(x["row"], y["row"]) for x, y in zip(by_row, by_row[1:]) if float(x["cost"]) < float(y["cost"])]
    sorted_desc = not inversions
    negatives = [r for r in numeric if float(r["cost"]) < 0]
    zeros = [r for r in numeric if float(r["cost"]) == 0]
    median = (costs[n // 2] if n % 2 else (costs[n // 2 - 1] + costs[n // 2]) / 2) if n else 0.0

    def top_share(k: int) -> float:
        return sum(costs[:k]) / total if total else 0.0

    cum, pareto_n = 0.0, None
    for i, c in enumerate(costs, start=1):
        cum += c
        if total and cum / total >= 0.80:
            pareto_n = i
            break

    small = [r for r in numeric if float(r["cost"]) < SMALL_VENDOR_THRESHOLD]
    small_total = sum(float(r["cost"]) for r in small)

    bands = [
        ("under $1,000", 0, 1_000),
        ("$1,000 to $9,999", 1_000, 10_000),
        ("$10,000 to $99,999", 10_000, 100_000),
        ("$100,000 to $999,999", 100_000, 1_000_000),
        ("$1,000,000 and above", 1_000_000, float("inf")),
    ]
    band_rows = []
    for label, lo, hi in bands:
        members = [float(r["cost"]) for r in numeric if lo <= float(r["cost"]) < hi]
        band_rows.append((label, len(members), sum(members)))
    if negatives:
        band_rows.insert(0, ("negative", len(negatives), sum(float(r["cost"]) for r in negatives)))

    dept_values = Counter(str(r["dept"]).strip() for r in named if not is_blank(r["dept"]))
    filled = {
        "dept": sum(1 for r in named if not is_blank(r["dept"])),
        "desc": sum(1 for r in named if not is_blank(r["desc"])),
        "sugg": sum(1 for r in named if not is_blank(r["sugg"])),
    }

    present = lambda lst: [x for x in lst if x in names_all]  # noqa: E731
    return dict(
        recs=recs, named=named, unnamed=unnamed, numeric=numeric,
        non_numeric_cost=non_numeric_cost, names=names, hygiene=hygiene,
        repairs=repairs, still_marked=still_marked,
        exact_dups=exact_dups, casefold_dups=casefold_dups, norm_dups=norm_dups,
        empty_key=empty_key, norm=norm, near=near, weak=weak_sorted,
        cost_formats=cost_formats, fractional=fractional, max_decimals=max_decimals,
        entity_tokens=entity_tokens, croatian_rows=croatian_rows,
        text_currency_hits=text_currency_hits, total=total, n=n, ranked=ranked,
        sorted_desc=sorted_desc, inversions=inversions, placeholder_recs=placeholder_recs,
        raw_only_hits=raw_only_hits, negatives=negatives, zeros=zeros, median=median,
        mean=(total / n if n else 0.0), min=(costs[-1] if n else 0.0), max=(costs[0] if n else 0.0),
        top_share=top_share, pareto_n=pareto_n, small=small, small_total=small_total,
        band_rows=band_rows, dept_values=dept_values, filled=filled,
        unique_names=len(set(names)),
        persons=present(OBSERVED_PERSON_NAMES),
        statutory=present(OBSERVED_STATUTORY),
        merchants=present(OBSERVED_CARD_MERCHANTS),
    )


def list_or_count(items: list[str], limit: int = 15) -> str:
    if not items:
        return "none"
    shown = "; ".join(f"`{x}`" for x in items[:limit])
    more = f" (and {len(items) - limit} more)" if len(items) > limit else ""
    return f"{len(items)}: {shown}{more}"


def render_main(a: dict, p: dict) -> list[str]:
    out = ["### Columns, types and blanks", ""]
    out += render_sheet_profile(p)
    out += ["", "### Row counts", ""]
    out.append(f"- Rows with any value below the header: {len(a['recs'])}")
    out.append(f"- Rows with a vendor name: {len(a['named'])} ({a['unique_names']} distinct name strings)")
    out.append(f"- Rows with a value but no vendor name: {len(a['unnamed'])}")
    out.append(f"- Rows with a numeric 12-month cost: {len(a['numeric'])}")
    out.append(f"- Rows with a vendor name but a non-numeric or blank cost: {len(a['non_numeric_cost'])}")
    if a["non_numeric_cost"]:
        out.append("  - " + "; ".join(f"row {r['row']} `{r['name']}` = `{r['cost']!r}`" for r in a["non_numeric_cost"][:20]))
    out.append(f"- Department filled: {a['filled']['dept']} of {len(a['named'])}; "
               f"Description filled: {a['filled']['desc']}; Suggestions filled: {a['filled']['sugg']}")
    if a["dept_values"]:
        out.append("  - Department values present: " + ", ".join(f"`{k}` ({v})" for k, v in a["dept_values"].most_common()))
    if a["sorted_desc"]:
        out.append("- Rows are sorted by cost, largest first (row number doubles as a spend rank)")
    else:
        inv = a["inversions"]
        pairs = ", ".join(f"{x} and {y}" for x, y in inv[:10])
        out.append(f"- Rows are sorted by cost, largest first, except for {len(inv)} adjacent pair(s) out of order "
                   f"(rows {pairs}); row number is an approximate spend rank")

    out += ["", "### Vendor name hygiene", ""]
    h = a["hygiene"]
    out.append(f"- Names matching Python's Title Case exactly: {pct(h['title_case_share'])} "
               "(the source applied Title Case to every name, so acronyms such as `Bdo Llp`, `Rsm Uk`, "
               "`Ss&C Intralinks`, `Dhl` and possessives such as `Kat'S Kitchen` are casing artifacts)")
    out.append(f"- Leading or trailing whitespace: {list_or_count(h['lead_trail_space'])}")
    out.append(f"- Internal double spaces: {list_or_count(h['double_space'])}")
    out.append(f"- ALL CAPS names: {list_or_count(h['all_caps'])}")
    out.append(f"- all lower-case names: {list_or_count(h['all_lower'])}")
    out.append(f"- Names containing digits (after mojibake repair): {list_or_count(h['has_digit'])}")
    out.append(f"- Names shorter than 3 characters: {list_or_count(h['short'])}")
    out.append(f"- Longest name: {h['max_len']} characters ({list_or_count(h['at_max_len'], 3)})")
    out.append(f"- Placeholder names: {list_or_count(h['placeholder'])}")
    out.append(f"- Names with non-ASCII characters: {list_or_count(h['non_ascii'])}")
    out.append(f"- Names with Excel `_xHHHH_` escapes (characters the source encoding could not store): {list_or_count(h['excel_escape'])}")
    out.append(f"- Names containing an em dash: {list_or_count(h['em_dash'])}")
    out.append(f"- Names with a parenthetical (alias, former name, region or unit): {list_or_count(h['parenthetical'])}")
    out.append(f"- Names with a ` - ` alias separator (brand vs legal entity or location): {list_or_count(h['dash_alias'])}")
    out.append(f"- Names with a hyphenated 2 to 5 letter tag right after the legal form (country tag, sometimes truncated): {list_or_count(h['trailing_suffix'])}")
    out.append(f"- Names ending in `..` (truncated in the source): {list_or_count(h['trailing_ellipsis'])}")
    out.append(f"- Names tagged `Supplier`: {list_or_count(h['supplier_tag'])}")
    out.append(f"- Card-statement style descriptors containing `*`: {list_or_count(h['card_descriptor'])}")

    out += ["", "**Encoding damage (mojibake)**", ""]
    out.append(f"{len(a['repairs'])} names contain UTF-8 text that was decoded as Windows-1252 and then Title Cased. "
               "The repair below (re-encode as cp1252, decode as UTF-8, fix the case of the letter after each "
               "repaired character) is proposed, not applied; each row should be eyeballed.")
    out.append("")
    if a["repairs"]:
        out += table(["Row", "As stored", "Proposed repair", "Cost"],
                     [[r, raw, fixed, money(c)] for r, raw, fixed, c in a["repairs"]])
    if a["still_marked"]:
        out.append("")
        out.append("Names with suspicious characters the automatic repair could not decode: " + list_or_count(a["still_marked"]))

    out += ["", "### Exact duplicate vendor names", ""]
    if a["exact_dups"]:
        out.append(f"{len(a['exact_dups'])} name strings appear more than once "
                   f"({sum(len(v) for v in a['exact_dups'].values())} rows in total).")
        out.append("")
        rows = [[k, len(v), ", ".join(str(r["row"]) for r in v), money(group_total(v))]
                for k, v in sorted(a["exact_dups"].items(), key=lambda kv: -group_total(kv[1]))]
        out += table(["Name", "Rows", "Row numbers", "Combined cost"], rows[:MAX_LIST_ROWS])
    else:
        out.append("None. Every one of the vendor name strings is unique.")
    out.append("")
    out.append("Case and whitespace-insensitive duplicates (same letters, different case or spacing): "
               + ("" if a["casefold_dups"] else "none."))
    for k, v in a["casefold_dups"].items():
        out.append(f"- {group_label(v)}")

    out += ["", "### Fuzzy duplicate vendor names", ""]
    out.append("Method: repair mojibake, strip accents, lower-case, replace `&` with `and`, collapse dotted "
               "abbreviations (`D.O.O.` to `doo`), drop punctuation, then drop legal-form tokens (Ltd, Limited, "
               "Inc, LLC, GmbH, D.O.O., J.D.O.O., D.D., Obrt, Bvba, Pvt, Private, Pty, Pte, Corp, Co, ...), "
               "geography tokens (Uk, Us, Ireland, India, Australia, Croatia, Zagreb, Split, London, International, "
               "Global, ...), stop words (the, and, of, za, i, u) and noise (`Supplier`). The remaining tokens form "
               "the matching key. Keys are a matching aid only; display names keep the original wording.")
    out.append("")
    out.append(f"**Tier 1: same key** ({len(a['norm_dups'])} groups). Almost certainly the same vendor billed "
               "through different legal entities, regions or spellings.")
    out.append("")
    if a["norm_dups"]:
        rows = [[k, group_label(v), money(group_total(v))]
                for k, v in sorted(a["norm_dups"].items(), key=lambda kv: -group_total(kv[1]))]
        out += table(["Key", "Names (row, cost)", "Combined cost"], rows[:MAX_LIST_ROWS])
    else:
        out.append("None.")
    if a["empty_key"]:
        out.append("")
        out.append("Names whose key is empty after normalization (only legal, geography or stop tokens): "
                   + group_label(a["empty_key"]))
    out.append("")
    out.append(f"**Tier 2: near matches between different keys** ({len(a['near'])} pairs). Rules: difflib ratio "
               f">= {FUZZY_RATIO:.2f} (similar spelling), one key's tokens all appear in the other (token subset), "
               "or at least two tokens shared covering half of the shorter key (shared tokens). Review candidates, "
               "not confirmed duplicates; some are distinct vendors of the same type, which matters for "
               "consolidation rather than deduplication.")
    out.append("")
    if a["near"]:
        rows = [[group_label(a["norm"][m["a"]]), group_label(a["norm"][m["b"]]), f"{m['ratio']:.2f}", m["rule"]]
                for m in a["near"]]
        out += table(["Vendor A (row, cost)", "Vendor B (row, cost)", "Ratio", "Rule"], rows[:MAX_LIST_ROWS])
        if len(rows) > MAX_LIST_ROWS:
            out.append(f"\n({len(rows) - MAX_LIST_ROWS} more pairs not shown)")
    else:
        out.append("None.")
    out.append("")
    out.append(f"**Tier 3: same leading token only** ({len(a['weak'])} groups with at least one pair not flagged above). Weak "
               "signal; listed because a shared brand word (Apple, Telefonica) or a shared Croatian noun "
               "(hotel, grad, ustanova) is worth one look.")
    out.append("")
    for t, ks in a["weak"]:
        members = [r for k in ks for r in a["norm"][k]]
        out.append(f"- `{t}`: {group_label(members)}")
    if not a["weak"]:
        out.append("None.")

    out += ["", "### Currency hints", ""]
    cost_header = p["columns"][COST_COL]["header"]
    out.append(f"- Cost column header: `{cost_header}`"
               + (" (states USD explicitly)." if "usd" in cost_header.lower() else " (no currency stated)."))
    out.append("- Excel number formats on numeric cost cells: "
               + ", ".join(f"`{k}`: {v}" for k, v in a["cost_formats"].most_common()))
    out.append(f"- Cost cells stored as text (would need parsing): {len(a['non_numeric_cost'])}")
    out.append(f"- Costs with a fractional part: {len(a['fractional'])} of {len(a['numeric'])}; "
               f"most decimal digits seen: {a['max_decimals']}. Invoice totals are rarely this precise, which is "
               "consistent with the values having been converted from other currencies or scaled (the brief says "
               "costs were modified). No FX rate, original currency or invoice date column exists, so the "
               "conversion cannot be checked or reversed.")
    out.append("- Currency symbols or ISO codes inside text cells (name, department, description, suggestions), "
               "checked after mojibake repair: "
               + (f"{len(a['text_currency_hits'])}: " + "; ".join(f"row {r} {k} `{v}`" for r, k, v in a["text_currency_hits"][:15])
                  if a["text_currency_hits"] else "none")
               + ((". Before repair " + "; ".join(f"row {r} `{v}`" for r, v in a["raw_only_hits"])
                   + " showed a stray currency sign that is encoding damage, not a currency.")
                  if a["raw_only_hits"] else ""))
    out.append("- Legal-form and geography tokens in vendor names (where the vendor is incorporated, which hints at "
               "the original billing currency but does not prove it): "
               + (", ".join(f"`{k}` ({v})" for k, v in a["entity_tokens"].most_common()) or "none"))
    out.append(f"- Rows with a Croatian legal form (D.O.O., J.D.O.O., D.D., Obrt): {a['croatian_rows']} of {len(a['named'])}")

    out += ["", "### Total 12-month spend and distribution", ""]
    out.append(f"- Total 12-month spend (sum of numeric costs): **{money(a['total'])}** across {a['n']} vendor rows "
               f"(exact: {a['total']:,.2f})")
    out.append(f"- Mean {money(a['mean'])}; median {money(a['median'])}; min {money(a['min'])}; max {money(a['max'])}")
    out.append(f"- Zero-cost rows: {len(a['zeros'])}; negative-cost rows: {len(a['negatives'])}"
               + ("" if not a["negatives"] else " (" + "; ".join(f"row {r['row']} `{r['name']}` {money(float(r['cost']))}" for r in a["negatives"][:10]) + ")"))
    out += ["", "**Top 10 vendors (as recorded, one row each)**", ""]
    rows, cum = [], 0.0
    for i, r in enumerate(a["ranked"][:10], start=1):
        c = float(r["cost"])
        cum += c
        rows.append([i, r["name"], r["row"], money(c), pct(c / a["total"]), pct(cum / a["total"])])
    out += table(["Rank", "Vendor", "Row", "12-month cost", "Share", "Cumulative"], rows)
    out += ["", "**Concentration**", ""]
    rows = [[f"Top {k}", money(sum(float(r["cost"]) for r in a["ranked"][:k])), pct(a["top_share"](k))]
            for k in (1, 10, 20, 50, 100) if k <= a["n"]]
    out += table(["Vendors", "Spend", "Share of total"], rows)
    out.append("")
    if a["pareto_n"]:
        out.append(f"The top {a['pareto_n']} vendors ({pct(a['pareto_n'] / a['n'])} of vendor rows) account for 80% of spend.")
    out += ["", f"**Vendors under {money(SMALL_VENDOR_THRESHOLD)}**", ""]
    out.append(f"- Count: {len(a['small'])} of {a['n']} vendor rows ({pct(len(a['small']) / a['n'] if a['n'] else 0)})")
    out.append(f"- Total spend: {money(a['small_total'])} ({pct(a['small_total'] / a['total'] if a['total'] else 0)} of total)")
    out += ["", "**Spend bands**", ""]
    rows = [[label, cnt, pct(cnt / a["n"] if a["n"] else 0), money(tot), pct(tot / a["total"] if a["total"] else 0)]
            for label, cnt, tot in a["band_rows"]]
    out += table(["Band", "Vendors", "Share of vendors", "Spend", "Share of spend"], rows)
    return out


# ---------------------------------------------------------------- observations and cleaning steps

def observations(a: dict, profiles: dict, departments: list[str]) -> list[str]:
    p = profiles[MAIN_SHEET]
    out = []
    out.append(f"- Vendor rows: {len(a['named'])}. The brief says about 400 vendors; consistent.")
    out.append(f"- The used range runs to row {p['max_row']} and column {get_column_letter(p['max_col'])}, but only "
               f"columns A to E carry a header and only rows 2 to {p['last_data_row']} carry data. The remaining "
               f"{p['trailing_blank_rows']} rows and {p['max_col'] - 5} columns are formatting only.")
    out.append("- `Department`, `1-line Description` and `Suggestions` are empty on every row: these three columns "
               "are the deliverable, to be produced as `outputs/vendors_classified.csv`.")
    out.append("- Costs are hard-coded values (no formulas), all numeric, labelled USD in the header and formatted as "
               "whole dollars in Excel while carrying up to "
               f"{a['max_decimals']} decimals underneath. Sums must use the underlying values, not the displayed ones.")
    if a["sorted_desc"]:
        out.append("- The sheet is sorted by cost, largest first, so row number minus one is the spend rank.")
    else:
        out.append(f"- The sheet is sorted by cost, largest first, apart from {len(a['inversions'])} adjacent pair(s) "
                   "out of order, so row number is only an approximate spend rank.")
    cfg = profiles.get(CONFIG_SHEET)
    if cfg:
        out.append(f"- `{CONFIG_SHEET}` lists {len(departments)} departments: " + ", ".join(f"`{d}`" for d in departments)
                   + ". " + (f"`{TAXONOMY_PATH}` exists." if TAXONOMY_PATH.exists()
                             else f"`{TAXONOMY_PATH}`, which CLAUDE.md names as the only allowed source of departments, does not exist yet."))
        out.append("- Several `Config` entries are spend categories rather than departments (`SaaS`, `Professional "
                   "Services`) and others overlap (`G&A` with `Finance`, `Legal`, `Facilities`). The taxonomy needs a "
                   "precedence rule before classification starts.")
    dv = [v for prof in profiles.values() for v in prof["validations"]]
    if dv:
        out.append("- Data validation rules in the workbook: " + "; ".join(dv) + ". The Department column is a dropdown "
                   "over the `Config` list, so department values must match `Config` character for character.")
    else:
        out.append("- Data validation rules in the workbook: none, so the Department column is free text and spelling "
                   "must be enforced by our own QA check.")
    out.append("- The template sheets ask for three opportunities (`Opportunity`, `Explanation`), a methodology note, "
               "and a memo of at most one page delivered as a Google Doc link. CLAUDE.md specifies `outputs/memo.md`; "
               "whether a Google Doc is also required is a question for the user.")
    return out


def cleaning_steps(a: dict, p: dict, departments: list[str]) -> list[str]:
    h = a["hygiene"]
    small_share = a["small_total"] / a["total"] if a["total"] else 0.0
    t1 = len(a["norm_dups"])
    t2 = len(a["near"])
    steps = [
        ("Work on a copy, never the raw file",
         f"Read `data/raw/vendor_analysis_assessment.xlsx` and write a cleaned table to `outputs/vendors_clean.csv`. "
         f"Record the raw file's SHA-256 (currently the value in this report's header) in the output and in a QA check "
         f"so any change to the raw file is detected. Give every row a stable id `V` plus its source row number "
         f"(`V0002` to `V{p['last_data_row']:04d}`) so every number downstream traces back to a source row."),
        ("Trim the used range",
         f"Keep rows 2 to {p['last_data_row']} ({len(a['named'])} vendor rows) and columns A to E. Drop the "
         f"{p['trailing_blank_rows']} trailing formatted-but-empty rows and the {p['max_col'] - 5} unnamed empty columns. "
         f"Assert the row count is exactly {len(a['named'])} after loading."),
        ("Keep costs as stored",
         f"Costs are numeric USD with up to {a['max_decimals']} decimals. Do not round the stored values; round only "
         f"for display (whole dollars). Assert the cleaned total equals {a['total']:,.2f} to the cent. "
         f"There are {len(a['zeros'])} zero and {len(a['negatives'])} negative values, so no sign handling is needed."),
        ("Repair encoding damage, keeping the original",
         f"Add `vendor_name_raw` (verbatim) and `vendor_name_clean`. Apply the cp1252 to UTF-8 repair shown in the "
         f"mojibake table to the {len(a['repairs'])} affected names, resolving Excel `_x008d_` escapes first, then "
         f"review each repair by eye. Strip accents only inside the matching key, never in the display name."),
        ("Handle the placeholder row",
         (f"{group_label(a['placeholder_recs'])} carries spend but no vendor name. Keep the spend in every total, "
          f"set the description to say the vendor name is missing in the source, and set `confidence=low`. "
          f"A department still has to be chosen from the taxonomy; propose `G&A` and flag it as unassignable.")
         if h["placeholder"] else "No placeholder vendor names found."),
        ("Tidy names for display without changing meaning",
         f"Remove the `Supplier` tag ({list_or_count(h['supplier_tag'])}), drop a trailing `..` truncation marker "
         f"({list_or_count(h['trailing_ellipsis'])}), and keep hyphenated country tags such as `-Uk` or the truncated "
         f"`-Greec` ({list_or_count(h['trailing_suffix'])}) out of the display name while noting them in a `name_notes` "
         f"column. Keep parentheticals and ` - ` aliases as they are, since they carry the alias or venue. Do not "
         f"expand truncated words; `Greec` stays an observation, not a correction."),
        ("Fix casing only through an explicit, reviewable map",
         "The source Title Cased every name. For display in the memo, maintain `qa/display_names.csv` mapping the raw "
         "name to a corrected display form for well-known acronyms and possessives (BDO LLP, RSM UK, SS&C, DHL, CBRE, "
         "HP, Kat's Kitchen, GoDaddy.com). Matching always uses the lower-cased key, never the display form, so this "
         "step cannot affect any number."),
        ("Decide duplicates explicitly and apply the merges in a mapping file",
         f"Create `qa/vendor_groups.csv` with one line per source row: `vendor_id`, `vendor_name_clean`, `group_key`, "
         f"`canonical_name`, `decision` (merge or keep), `reason`. Merge the {t1} Tier 1 groups by default; review the "
         f"{t2} Tier 2 pairs one by one (the two Navan rows are the same company and together would be the second "
         f"largest vendor; Tmforum and Tm Forum, Hr Solution and Hrsolution, the four Apple entities, DHL and Bupa "
         f"are the same vendor families; the student centres, occupational-health clinics and hotels are different "
         f"vendors of the same type and belong in consolidation analysis, not in a merge). Report spend both per "
         f"source row and per canonical vendor so both views trace to the raw rows."),
        ("Add a Croatian glossary before classifying",
         f"{a['croatian_rows']} rows carry a Croatian legal form and many names describe the business in Croatian "
         f"(savjetovanje, odvjetnicko drustvo, medicina rada, prijevoz, dostava, ugostiteljstvo, osiguranje, studentski "
         f"centar, gradski ured). Write `docs/glossary_hr.md` listing each term used and its English meaning so "
         f"descriptions for those rows are translations, not guesses."),
        ("Flag names that cannot be classified from the name alone",
         ("Names that read as individuals (" + ", ".join(f"`{x}`" for x in a["persons"]) + "), " if a["persons"] else "")
         + ("statutory or government payees (" + ", ".join(f"`{x}`" for x in a["statutory"]) + "), " if a["statutory"] else "")
         + ("and retail or card-statement merchants (" + ", ".join(f"`{x}`" for x in a["merchants"]) + ") " if a["merchants"] else "")
         + "get `confidence=low` and a description that says what can and cannot be inferred. Statutory payees do not "
           "fit Terminate, Consolidate or Optimize; ask the user whether to add a fourth label or to use Optimize with "
           "a `no action, statutory` rationale."),
        ("Treat the long tail as a batch, not individually",
         f"{len(a['small'])} rows ({pct(len(a['small']) / a['n'] if a['n'] else 0)} of rows) are under "
         f"{money(SMALL_VENDOR_THRESHOLD)} and together total {money(a['small_total'])} ({pct(small_share)} of spend). "
         f"Every row still gets a department, description and recommendation, but classify them in batches and do not "
         f"let them drive the memo. Any savings claimed on them must be the computed sum, not an estimate."),
        ("Create the taxonomy from the workbook's own list",
         f"Write `{TAXONOMY_PATH}` with the {len(departments)} `Config` departments verbatim, a one-line definition each, "
         f"inclusion examples from this vendor list, and a precedence rule for overlaps (for example: a tool used by one "
         f"team goes to that team, a company-wide tool goes to `SaaS`; outside counsel goes to `Legal`, not `Professional "
         f"Services`; rent and coworking go to `Facilities`, not `G&A`). Classification cannot start before this file exists."),
        ("Automate the QA checks",
         f"A `qa/check_outputs.py` script that asserts: {len(a['named'])} rows in and out; total spend equals the raw "
         f"total to the cent; every department is in `{TAXONOMY_PATH}`; every recommendation is one of Terminate, "
         f"Consolidate, Optimize with a one-sentence rationale; no banned phrase appears in any description; no em dash "
         f"appears in any output file; every savings figure in the memo matches a value in `outputs/analysis/`."),
    ]
    out = []
    for i, (title, body) in enumerate(steps, start=1):
        out.append(f"{i}. **{title}.** {body}")
    return out


# ---------------------------------------------------------------- main

def main(argv: list[str]) -> int:
    raw = Path(argv[1]) if len(argv) > 1 else RAW_DEFAULT
    out_path = Path(argv[2]) if len(argv) > 2 else OUT_DEFAULT
    digest = sha256(raw)

    with open(raw, "rb") as fh:  # binary handle: openpyxl cannot write back to it
        wb = load_workbook(fh, data_only=True)
    with open(raw, "rb") as fh:
        wb_formulas = load_workbook(fh, data_only=False)

    profiles = {ws.title: profile_sheet(ws, wb_formulas[ws.title]) for ws in wb.worksheets}
    a = analyze_main(wb[MAIN_SHEET], profiles[MAIN_SHEET])
    departments = ([str(v) for coord, v in profiles[CONFIG_SHEET]["cells"] if coord != "A1"]
                   if CONFIG_SHEET in profiles else [])
    defined_names = list(wb.defined_names.keys()) if hasattr(wb.defined_names, "keys") else []

    lines: list[str] = []
    lines.append(f"# Data profile: {raw.name}")
    lines.append("")
    lines.append(f"Generated {date.today().isoformat()} by `scripts/00_data_profile.py`. The workbook was opened "
                 f"read-only and not modified. Source SHA-256: `{digest}`.")
    lines.append("")
    lines.append("## 1. Workbook overview")
    lines.append("")
    rows = []
    for title, p in profiles.items():
        named_cols = sum(1 for c in p["columns"] if c["header"] != "(no header)")
        rows.append([title, p["dims"], p["rows_with_values"], p["data_rows"], f"{named_cols} of {p['max_col']}", p["formula_cells"]])
    lines += table(["Sheet", "Used range", "Rows with values", "Data rows (below header)", "Named columns", "Formula cells"], rows)
    lines.append("")
    lines.append(f"Sheets: {len(profiles)}, all visible. Defined names: "
                 + (", ".join(f"`{d}`" for d in defined_names) if defined_names else "none") + ".")
    lines.append("")
    lines.append(f"## 2. Sheet `{MAIN_SHEET}`")
    lines.append("")
    lines += render_main(a, profiles[MAIN_SHEET])
    lines.append("")

    section = 3
    for title, p in profiles.items():
        if title == MAIN_SHEET:
            continue
        lines.append(f"## {section}. Sheet `{title}`")
        lines.append("")
        lines += render_sheet_profile(p)
        lines.append("")
        lines.append("Non-blank cells, verbatim:")
        lines.append("")
        for coord, v in p["cells"]:
            lines.append(f"- `{coord}`: {md_escape(str(v).replace(chr(10), '<br>'))}")
        lines.append("")
        section += 1

    lines.append(f"## {section}. Observations that affect the analysis")
    lines.append("")
    lines += observations(a, profiles, departments)
    lines.append("")
    section += 1
    lines.append(f"## {section}. Proposed cleaning steps")
    lines.append("")
    lines += cleaning_steps(a, profiles[MAIN_SHEET], departments)
    lines.append("")

    text = "\n".join(lines)
    if EM_DASH in text:
        bad = [ln for ln in lines if EM_DASH in ln][:3]
        raise SystemExit("Output contains an em dash; refusing to write. First offending lines: " + " || ".join(bad))
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(text, encoding="utf-8")

    print(f"wrote {out_path} ({len(text):,} chars, {len(lines)} lines)")
    print(f"vendor rows: {len(a['named'])}; numeric costs: {a['n']}; total spend: {money(a['total'])}")
    print(f"mojibake repairs: {len(a['repairs'])}; exact dups: {len(a['exact_dups'])}; "
          f"tier1: {len(a['norm_dups'])}; tier2: {len(a['near'])}; tier3 groups: {len(a['weak'])}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
