#!/usr/bin/env python3
"""Shared helpers for the vendor spend analysis scripts.

Anything that must behave identically across steps lives here: opening the raw
workbook read-only, the mojibake repair, the matching key, the near-duplicate
candidate search, the entity merge decisions, the workbook structure audit,
money formatting, and the guard that refuses to write an em dash.

Scripts import this module after putting their own directory on sys.path, so
they also work under `python -I`.
"""
from __future__ import annotations

import hashlib
import re
import unicodedata
import xml.etree.ElementTree as ET
import zipfile
from collections import defaultdict
from difflib import SequenceMatcher
from pathlib import Path

from openpyxl import load_workbook
from openpyxl.utils import get_column_letter, range_boundaries

ROOT = Path(__file__).resolve().parent.parent
RAW_PATH = ROOT / "data" / "raw" / "vendor_analysis_assessment.xlsx"
MAIN_SHEET = "Vendor Analysis Assessment"
CONFIG_SHEET = "Config"
FUZZY_RATIO = 0.85
EM_DASH = "\u2014"
EN_DASH = "\u2013"


# ---------------------------------------------------------------- basic helpers

def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def open_workbook(path: Path = RAW_PATH, data_only: bool = True):
    """Load from a binary handle: openpyxl can never write back to the file."""
    with open(path, "rb") as fh:
        return load_workbook(fh, data_only=data_only)


def is_blank(v) -> bool:
    return v is None or (isinstance(v, str) and v.strip() == "")


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


def assert_no_dashes(text: str, label: str) -> None:
    for ch, name in ((EM_DASH, "em dash"), (EN_DASH, "en dash")):
        if ch in text:
            bad = [ln for ln in text.splitlines() if ch in ln][:3]
            raise SystemExit(f"{label} contains an {name}; refusing to write. First lines: " + " || ".join(bad))


def write_text(path: Path, text: str) -> None:
    assert_no_dashes(text, str(path))
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def rel(path: Path) -> str:
    try:
        return str(Path(path).resolve().relative_to(ROOT))
    except ValueError:
        return str(path)


# ---------------------------------------------------------------- name tokens

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
    """Matching key: repaired, accent-free, lower-case, without legal forms,
    geography, stop words or noise. Used for matching only, never for display."""
    s = strip_accents(repair_mojibake(name)[0]).lower()
    s = s.replace("&", " and ")
    s = re.sub(r"\ba/s\b", " as ", s)
    s = re.sub(r"\b((?:[a-z]\.){2,})", lambda m: m.group(1).replace(".", ""), s)  # d.o.o. -> doo
    s = re.sub(r"\bsp\.?\s*z\s*o\.?\s*o\b\.?", " spzoo ", s)
    s = re.sub(r"[^a-z0-9 ]+", " ", s)
    drop = LEGAL_TOKENS | GEO_TOKENS | STOP_TOKENS | NOISE_TOKENS
    return " ".join(t for t in s.split() if t not in drop)


# ---------------------------------------------------------------- near-duplicate candidates

def group_label(recs: list[dict]) -> str:
    return "; ".join(
        f"`{r['name']}` (row {r['row']}, {money(float(r['cost'])) if is_number(r['cost']) else 'cost n/a'})"
        for r in recs
    )


def group_total(recs: list[dict]) -> float:
    return sum(float(r["cost"]) for r in recs if is_number(r["cost"]))


def near_duplicate_candidates(named: list[dict]) -> dict:
    """Tiered near-duplicate search over records with 'name', 'row', 'cost'.

    Tier 1: identical matching key. Tier 2: different keys with similar
    spelling, a token subset, or two or more shared tokens covering half of the
    shorter key. Tier 3: same leading token where some pair was not already
    flagged. Sets r['key'] on every record.
    """
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
    return {"norm": norm, "norm_dups": norm_dups, "empty_key": empty_key, "near": near, "weak": weak_sorted}


# ---------------------------------------------------------------- vendor records

def load_vendor_records(path: Path = RAW_PATH) -> list[dict]:
    """One record per vendor row of the main sheet, in sheet order."""
    ws = open_workbook(path)[MAIN_SHEET]
    out = []
    for row in ws.iter_rows(min_row=2, max_row=ws.max_row, max_col=3):
        name, _dept, cost = (c.value for c in row)
        if is_blank(name) and is_blank(cost):
            continue
        r = row[0].row
        fixed, changed = repair_mojibake(str(name))
        out.append({
            "vendor_id": f"V{r:04d}",
            "row": r,
            "name": str(name),
            "name_fixed": fixed,
            "mojibake": changed,
            "cost": cost,
        })
    return out


# ---------------------------------------------------------------- entity merges and links
# Policy (decision of 2026-11-10, docs/decisions.md): merge only when it is the
# same vendor relationship under a changed or variant name (a rename, a
# spelling variant, the same contract moved between entities). Where entities
# share a parent or brand but supply different products or contracts, or share
# a lineage, record a link instead. MERGE_GROUPS and LINK_GROUPS are the source
# of truth for qa/vendor_groups.csv.

MERGE_GROUPS = [
    {"canonical": "Navan", "rows": [3, 24], "status": "merge", "confidence": "high",
     "relationship": "renamed entity",
     "reason": "TripActions Inc renamed itself Navan Inc in 2023; both rows are the same travel and expense platform"},
    {"canonical": "AWS", "rows": [14, 103], "status": "merge", "confidence": "high",
     "relationship": "same service, entity name variant",
     "reason": "one AWS relationship, the same cloud service and customer agreement, billed under the Inc. and LLC entity names"},
    {"canonical": "TM Forum", "rows": [25, 249], "status": "merge", "confidence": "high",
     "relationship": "spelling variant",
     "reason": "Tmforum and Tm Forum are two spellings of the same association"},
    {"canonical": "4i", "rows": [17, 72], "status": "proposed merge", "confidence": "medium",
     "relationship": "same group, other entity",
     "reason": "shared and unusual 4i brand, both advisory or consulting in India; to be confirmed or reversed by web verification"},
]

LINK_GROUPS = [
    {"label": "Salesforce", "rows": [2, 173], "type": "shared parent",
     "reason": "Slack has been a Salesforce company since 2021, so it goes into the same renewal"},
    {"label": "Atlassian", "rows": [91, 297], "type": "shared parent",
     "reason": "Trello is an Atlassian product"},
    {"label": "SolarWinds", "rows": [130, 311], "type": "shared parent",
     "reason": "Papertrail is a SolarWinds product"},
    {"label": "Microsoft", "rows": [26, 81, 125], "type": "shared parent",
     "reason": "LinkedIn and npm (through GitHub) are Microsoft companies"},
    {"label": "ICICI group", "rows": [95, 143], "type": "shared parent",
     "reason": "ICICI Lombard (general insurance) and ICICI Prudential (life insurance) are separate ICICI group insurers"},
    {"label": "Amazon", "rows": [14, 103, 203, 291], "type": "shared parent",
     "reason": "AWS and the Amazon marketplaces in the UK and Australia share a parent but are different services and purchases"},
    {"label": "Apple", "rows": [123, 172, 175, 229], "type": "same brand, separate entities",
     "reason": "four Apple regional entities (UK retail, Australia, Ireland, Americas) with separate purchases"},
    {"label": "Bupa", "rows": [47, 71], "type": "same brand, separate entities",
     "reason": "two Bupa entities with separate insurance contracts, one of them Bupa Australia"},
    {"label": "HR Solution International", "rows": [16, 90], "type": "same brand, separate entities",
     "reason": "a GmbH and an AG, so two legal entities and presumably two country contracts; a merge only if one contract moved between them"},
    {"label": "Acclime", "rows": [99, 105], "type": "same brand, separate entities",
     "reason": "Acclime's corporate services entity and its US entity, presumably separate engagements"},
    {"label": "DHL", "rows": [303, 336], "type": "same brand, separate entities",
     "reason": "a bare DHL record and DHL Express (UK); the file does not show that they are one account"},
    {"label": "Telef\u00f3nica", "rows": [15, 93], "type": "same brand, separate entities",
     "reason": "two Telef\u00f3nica group entities (Global Services GmbH, Compras Electr\u00f3nicas S.L.); what each payment is goes to Finance"},
    {"label": "Allianz Australia", "rows": [94, 212], "type": "same brand, separate entities",
     "reason": "Allianz workers' compensation in Victoria and, by the Wa suffix, Western Australia: separate state policies (decision of 2026-11-10)"},
    {"label": "GRT Hotels & Resorts", "rows": [171, 190], "type": "same brand, separate entities",
     "reason": "two hotels of the GRT group; the Radisson row names itself a unit of GRT Hotels & Resorts"},
    {"label": "Sodexo and Pluxee", "rows": [54, 128], "type": "same lineage",
     "reason": "Pluxee was demerged from Sodexo in 2024; on-site catering and meal cards are different services and contracts (decision of 2026-11-10)"},
]

# Candidate sets from the string search that are reviewed and neither merged nor linked.
DISTINCT_VERDICTS = [
    ([30, 86, 186], "different vendors, same type",
     "three different university student centres (Zagreb, Split, Karlovac) offering the same student-work service"),
    ([73, 139], "different vendors", "two different cities (Zagreb, Split)"),
    ([88, 99, 105], "different vendors, same type",
     "Intertrust and Acclime both sell corporate secretarial services; only the words Corporate Services are shared"),
    ([74, 330], "different vendors", "unrelated firms whose names both contain poslovno savjetovanje (business consulting)"),
    ([192, 197], "different vendors, same type", "two different recreation clubs"),
    ([382, 383], "different vendors, same type", "two occupational-medicine practices run by different doctors"),
    ([348, 372], "different vendors", "share only the words Garden and City"),
    ([46, 360], "different vendors", "share only the word New"),
    ([53, 318], "different vendors", "share only Hrvatski (Croatian)"),
    ([82, 233], "different vendors, same type", "two different caterers"),
    ([183, 315], "different vendors, same type", "two painting-event sole traders with different owners"),
    ([247, 304], "different vendors, same type", "two different hotels"),
    ([328, 384], "different vendors, same type", "two different health institutions"),
]


def merge_group_of(row: int) -> dict | None:
    return next((g for g in MERGE_GROUPS if row in g["rows"]), None)


def link_group_of(row: int) -> dict | None:
    return next((g for g in LINK_GROUPS if row in g["rows"]), None)


def verdict_for(rows: set[int]) -> tuple[str, str]:
    """Verdict for a candidate set of source rows; raises if unreviewed."""
    for g in MERGE_GROUPS:
        if rows <= set(g["rows"]):
            return f"{g['status']} into {g['canonical']}", g["reason"]
    for g in LINK_GROUPS:
        if rows <= set(g["rows"]):
            return f"link: {g['label']} ({g['type']})", g["reason"]
    for grp, verdict, reason in DISTINCT_VERDICTS:
        if rows <= set(grp):
            return verdict, reason
    raise KeyError(f"no verdict recorded for rows {sorted(rows)}")


# ---------------------------------------------------------------- structure audit

_M = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
_R = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}"
_P = "{http://schemas.openxmlformats.org/package/2006/relationships}"


def _resolve_color(color) -> str | None:
    if color is None:
        return None
    if color.type == "rgb":
        return str(color.rgb).upper()
    if color.type == "theme":
        return f"theme{color.theme}"
    if color.type == "indexed":
        return f"indexed{color.indexed}"
    return None


def structure_audit(path: Path = RAW_PATH) -> dict:
    """Facts about the workbook structure from openpyxl and the raw package XML.

    openpyxl does not surface built-in defined names, extension-list (x14)
    validation and conditional formats, or threaded comments, so those are
    read from the XML directly.
    """
    wb = open_workbook(path)
    with zipfile.ZipFile(path) as z:
        parts = z.namelist()
        raw = {n: z.read(n) for n in parts}
    wb_root = ET.fromstring(raw["xl/workbook.xml"])
    rels = {r.get("Id"): r.get("Target")
            for r in ET.fromstring(raw["xl/_rels/workbook.xml.rels"]).iter(_P + "Relationship")}
    sheet_part, raw_state = {}, {}
    for s in wb_root.iter(_M + "sheet"):
        target = rels[s.get(_R + "id")]
        sheet_part[s.get("name")] = target.lstrip("/") if target.startswith("/") else "xl/" + target
        raw_state[s.get("name")] = s.get("state", "visible")
    defined = [{"name": d.get("name"), "hidden": d.get("hidden") in ("1", "true"),
                "scope": d.get("localSheetId"), "ref": d.text}
               for d in wb_root.iter(_M + "definedName")]

    referenced = set()
    sheets = []
    for ws in wb.worksheets:
        x = raw[sheet_part[ws.title]].decode("utf-8")
        for m in re.finditer(r'<c [^>]*t="s"[^>]*>\s*<v>(\d+)</v>', x):
            referenced.add(int(m.group(1)))
        cells = [c for row in ws.iter_rows() for c in row]
        valued = [c for c in cells if not is_blank(c.value)]
        last_row = max((c.row for c in valued), default=0)
        last_col = max((c.column for c in valued), default=0)
        white_font, invisible, hidden_fmt, sizes = [], [], [], []
        for c in valued:
            font = _resolve_color(c.font.color)
            fill = _resolve_color(c.fill.fgColor) if c.fill is not None and c.fill.fill_type else None
            if font in ("FFFFFFFF", "theme0"):
                white_font.append((c.coordinate, fill))
                if fill in (None, "FFFFFFFF", "theme0"):
                    invisible.append(c.coordinate)
            elif font is not None and fill is not None and font == fill:
                invisible.append(c.coordinate)
            if ";;;" in str(c.number_format):
                hidden_fmt.append(c.coordinate)
            if c.font.sz is not None:
                sizes.append(float(c.font.sz))
        dvs = [{"sqref": str(dv.sqref), "type": dv.type, "formula1": dv.formula1,
                "allow_blank": bool(dv.allow_blank), "error_alert": bool(dv.showErrorMessage)}
               for dv in ws.data_validations.dataValidation]
        dv_cols = set()
        for dv in ws.data_validations.dataValidation:
            for rng in dv.sqref.ranges:
                min_col, _, max_col, _ = range_boundaries(str(rng))
                dv_cols.update(range(min_col, max_col + 1))
        styled_beyond_rows = sum(1 for c in cells if c.row > last_row and c.has_style)
        styled_beyond_cols = sum(1 for c in cells if c.row <= last_row and c.column > last_col and c.has_style)
        sheets.append({
            "title": ws.title,
            "state": ws.sheet_state,
            "raw_state": raw_state.get(ws.title),
            "dims": ws.dimensions,
            "max_row": ws.max_row,
            "max_col": ws.max_column,
            "last_row": last_row,
            "last_col": last_col,
            "values": len(valued),
            "cell_elements": len(re.findall(r"<c [^>]*?(?:/>|>)", x)),
            "styled_beyond_rows": styled_beyond_rows,
            "styled_beyond_cols": styled_beyond_cols,
            "hidden_rows": [r for r, d in ws.row_dimensions.items() if d.hidden],
            "zero_height_rows": [r for r, d in ws.row_dimensions.items() if d.ht is not None and float(d.ht) == 0],
            "outline_rows": [r for r, d in ws.row_dimensions.items() if d.outlineLevel],
            "hidden_cols": [k for k, d in ws.column_dimensions.items() if d.hidden],
            "zero_width_cols": [k for k, d in ws.column_dimensions.items() if d.customWidth and d.width is not None and float(d.width) == 0],
            "outline_cols": [k for k, d in ws.column_dimensions.items() if d.outlineLevel],
            "comments": sum(1 for c in cells if c.comment is not None),
            "hyperlinks": [(c.coordinate, c.hyperlink.target) for c in cells if c.hyperlink is not None],
            "merged": len(ws.merged_cells.ranges),
            "images": len(ws._images),
            "charts": len(ws._charts),
            "cf_rules": sum(len(cf.rules) for cf in ws.conditional_formatting),
            "raw_cf": x.count("<conditionalFormatting") + x.count("<x14:conditionalFormatting"),
            "dvs": dvs,
            "dv_cols": sorted(dv_cols),
            "raw_dv": len(re.findall(r"<dataValidation[ >]", x)),
            "raw_x14_dv": x.count("<x14:dataValidation"),
            "formulas": len(re.findall(r"<f[ >]", x)),
            "legacy_drawing": "<legacyDrawing" in x,
            "autofilter": ws.auto_filter.ref,
            "filter_columns": len(ws.auto_filter.filterColumn),
            "sort_state": ws.auto_filter.sortState is not None or "<sortState" in x,
            "protected": bool(ws.protection.sheet),
            "freeze": ws.freeze_panes,
            "white_font": white_font,
            "invisible": invisible,
            "hidden_numfmt": hidden_fmt,
            "min_font": min(sizes) if sizes else None,
            "sheet_format": re.findall(r"<sheetFormatPr ([^>]*?)/?>", x),
        })

    sst = ET.fromstring(raw["xl/sharedStrings.xml"]) if "xl/sharedStrings.xml" in raw else None
    sst_total = len(sst.findall(_M + "si")) if sst is not None else 0
    drawings = [p for p in parts if p.startswith("xl/drawings/") and p.endswith(".xml")]
    persons = "xl/persons/person.xml" in raw
    return {
        "path": path,
        "sheets": sheets,
        "defined_names": defined,
        "user_defined_names": [d for d in defined if not str(d["name"]).startswith("_xlnm.")],
        "builtin_names": [d for d in defined if str(d["name"]).startswith("_xlnm.")],
        "openpyxl_names": list(wb.defined_names.keys()),
        "workbook_protected": wb.security is not None and bool(getattr(wb.security, "lockStructure", False)),
        "parts": parts,
        "docprops": [p for p in parts if p.startswith("docProps/")],
        "comment_parts": [p for p in parts if "comment" in p.lower()],
        "persons_part": persons,
        "persons_listed": len(re.findall(rb"<\w+:person\b", raw["xl/persons/person.xml"])) if persons else 0,
        "drawing_parts": drawings,
        "drawings_with_content": [p for p in drawings if re.search(rb"(twoCellAnchor|oneCellAnchor|absoluteAnchor)", raw[p])],
        "macros": [p for p in parts if "vbaproject" in p.lower()],
        "external_links": [p for p in parts if p.startswith("xl/externalLinks/")],
        "pivots": [p for p in parts if "pivot" in p.lower()],
        "embeddings": [p for p in parts if p.startswith("xl/embeddings/")],
        "custom_xml": [p for p in parts if p.startswith("customXml/")],
        "shared_strings": sst_total,
        "shared_strings_referenced": len(referenced),
        "shared_strings_unreferenced": sst_total - len(referenced & set(range(sst_total))),
    }


def main_sheet(facts: dict) -> dict:
    return next(s for s in facts["sheets"] if s["title"] == MAIN_SHEET)


def data_range(s: dict) -> str:
    return f"A1:{get_column_letter(s['last_col'])}{s['last_row']}"
