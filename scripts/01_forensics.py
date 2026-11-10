#!/usr/bin/env python3
"""Forensic pass over the raw vendor workbook. No classification.

Checks the workbook structure, then the vendor rows: identical amounts, cost
precision, first digits, row order, near-duplicate names and payee types.
Every finding states what it implies for classification or for the memo.

Writes outputs/analysis/01_forensics.md and outputs/analysis/01_forensic_flags.csv.
The raw workbook is opened read-only; its SHA-256 is checked before and after.

Usage: python scripts/01_forensics.py
"""
from __future__ import annotations

import bisect
import csv
import io
import math
import re
import sys
from collections import Counter, defaultdict
from datetime import date
from decimal import Decimal
from pathlib import Path

from openpyxl.utils import get_column_letter

sys.path.insert(0, str(Path(__file__).resolve().parent))
from vsa_common import (  # noqa: E402
    LINK_GROUPS, MERGE_GROUPS, RAW_PATH, ROOT, data_range, load_vendor_records, main_sheet,
    money, near_duplicate_candidates, pct, rel, sha256, strip_accents, structure_audit, table,
    verdict_for, write_text,
)

OUT_MD = ROOT / "outputs" / "analysis" / "01_forensics.md"
OUT_CSV = ROOT / "outputs" / "analysis" / "01_forensic_flags.csv"
SMALL = 1_000.0
MATERIAL = 5_000.0
NIGRINI_FIRST_DIGIT = [(0.006, "close conformity"), (0.012, "acceptable conformity"),
                       (0.015, "marginally acceptable conformity"), (float("inf"), "nonconformity")]
# Subgroups that are non-discretionary under docs/recommendation_rules.md and so
# stay out of the savings base. Student centres (labour) and utilities (ordinary
# bills) are deliberately not here, and neither are the Supplier-tagged names.
STATUTORY_SUBGROUPS = ("Tax authority", "Government and municipal bodies", "Regulators and statutory schemes",
                       "Workers' compensation (statutory)", "Occupational health")
CUSTOMER_MANDATED_SUBGROUPS = ("Customer procurement entities", "Customer-mandated supplier network")

# ---------------------------------------------------------------- payee-type flags
# (category, subgroup, regex on the repaired, accent-free name, expected matches, evidence).
# Flags describe what a name shows; they are not departments. A vendor can carry
# flags in several categories. The expected count guards against a pattern
# silently matching more or fewer rows than intended.
FLAG_RULES = [
    ("Individuals and owner-named businesses", "Bare personal name",
     r"^(Stipe Piric|John Smith|Fabiola Thistlewhaite|George Anchor|Susan Lee|Ansar Madovic)$", 6,
     "a given name and a surname with no business word or legal form"),
    ("Individuals and owner-named businesses", "Single surname-like word",
     r"^(Livingstone|Crossland)$", 2,
     "one surname-like word; a person cannot be told apart from a business"),
    ("Individuals and owner-named businesses", "Business carrying its owner's name",
     r"Vl\. |A Unit Of |Ordinacija Medicine Rada|Medicinu Rada I Sporta Dr\.", 6,
     "vl. (vlasnik, owner), a unit of a named person, or a medical practice named after its doctor"),
    ("Individuals and owner-named businesses", "Croatian sole trader (obrt)",
     r"\bObrt\b", 5, "obrt is a Croatian sole-trader business owned by one person"),

    ("Consumer or retail purchases", "Apple",
     r"^Apple\b", 4, "Apple retail or Apple regional entities; may be employee IT equipment"),
    ("Consumer or retail purchases", "Amazon marketplace",
     r"^Amazon\.Co\.Uk$|^Amazon \(Aus\)$", 2, "Amazon consumer marketplace in the UK and Australia"),
    ("Consumer or retail purchases", "Supermarkets and food retail",
     r"^(Konzum Plus|Spar Hrvatska|Coles|M&S Simply Food)\b", 4, "supermarket chains in Croatia, Australia and the UK"),
    ("Consumer or retail purchases", "General, electronics and online retail",
     r"^(Currys Pc World|Ikea Hrvatska|Pepco Croatia|Notino|Ekupi|Sport Vision|Farmacia|Muller Trgovina|"
     r"Officeworks|Snappy Snaps|Pink Ribbon Shop)\b", 11,
     "high-street or online retailers, a pharmacy and a photo shop"),
    ("Consumer or retail purchases", "Restaurants, cafes, bakeries, caterers and food delivery",
     r"^(Pret A Manger|Uber \*Eats|Wolt Enterprises|Axil Coffee Roasters|Bakemono Bakers|Cupcake Central|Pan-Pek|"
     r"Oakberry|Kat'S Kitchen|The Cook Kitchen|Soho Kitchen|The Riding House Cafe|Gaucho Restaurants|"
     r"Tattu Manchester|Pepe'S Italian|Magic Mountain Saloon|Taste Of Health|My Foodiverse|Lunch Nutrition|"
     r"Catering Muring|Catering Ivic|City Pantry|Istra Wine|Vivat Fina Vina|Obrt Za Ugostiteljstvo)", 25,
     "food or drink in the name, or a known food brand"),
    ("Consumer or retail purchases", "Gifts and flowers",
     r"^(Floom|Prezzee|Regency Hampers)\b", 3, "flower delivery, gift cards and hampers"),
    ("Consumer or retail purchases", "Gyms, sports cards and recreation clubs",
     r"^(Gym4You|Friends Sports Club|Chamiers Recreation Club|P S Recreation Club|The Cycle Gap|"
     r"Sportska Udruga Split|Benefit Systems)\b", 7,
     "gym, fitness studio or sports club in the name; Benefit Systems sells the MultiSport card (analyst hint)"),

    ("Government, tax, court and regulator payees", "Tax authority",
     r"^Australian Taxation Office", 1, "the Australian Taxation Office"),
    ("Government, tax, court and regulator payees", "Government and municipal bodies",
     r"^(Cayman Islands Government|Grad Split$|Grad Zagreb)", 3,
     "a national government and two Croatian cities (grad means city)"),
    ("Government, tax, court and regulator payees", "Regulators and statutory schemes",
     r"^(Ico|Icare Nsw)$|^National Securities Depository", 3,
     "Ico, presumably the UK data-protection regulator (ICO); the NSW workers' insurance agency (icare); India's securities depository (NSDL)"),
    ("Government, tax, court and regulator payees", "Public institutions",
     r"Studentski Centar|^Nastavni Zavod Za Javno Zdravstvo", 4,
     "university student centres and a public health institute"),
    ("Government, tax, court and regulator payees", "Publicly owned utilities",
     r"^(Zagrebacki Holding|Hep Elektra)", 2,
     "the City of Zagreb's utility holding company and the state power group's electricity supplier"),

    ("Memberships and associations", "Industry and community associations",
     r"^(Tmforum|Tm Forum|Hrvatski Nezavisnici Izvoznici Softvera|Split Tech City)$", 4,
     "telecom industry body, Croatian software exporters' association, Split tech community"),
    ("Memberships and associations", "Professional and learning memberships",
     r"^(Pmi Global Operations Center|Interaction Design Foundation|Smashing Media)", 3,
     "Project Management Institute, a UX learning membership, a UX publisher and conference organiser"),
    ("Memberships and associations", "Sports and recreation clubs",
     r"^(Chamiers Recreation Club|P S Recreation Club|Friends Sports Club|Sportska Udruga Split)$", 4,
     "club in the name (udruga means association)"),

    ("Agencies and recruiters", "Recruitment agencies",
     r"^(Harmonic Group|Mason Frank International|Accutrainee|Technet It Recruitment|Cedar Recruitment|"
     r"Integrated Personnel Services)", 6, "recruitment or personnel in the name, or analyst hint"),
    ("Agencies and recruiters", "Job boards and recruiting platforms",
     r"^(Linkedin Ireland|Info Edge India)", 2, "LinkedIn and Info Edge (Naukri), per analyst hints"),
    ("Agencies and recruiters", "Employer of record, payroll and HR outsourcing",
     r"^(Hr Solution International|Hrsolution International|Australian Payroll Professionals|Radius Group)", 4,
     "payroll or HR outsourcing, per the name or analyst hint"),
    ("Agencies and recruiters", "Marketing, PR and media agencies",
     r"^(Big Frontier|Mightyhive|Carrington Communications|Cision Pr Newswire|Media Promo Plus|Puzzle Promotion|"
     r"Digitalna Produkcija)", 7, "agency, PR, promotion or production in the name, or analyst hint"),
    ("Agencies and recruiters", "Event organisers and agencies",
     r"^(Terrapinn|Blink Events|Urbani Eventi|Event Ors|Rishi Events|Djs For U|Lajnap Comedy Booking|"
     r"Entrio Tehnologije)", 8, "events, bookings or ticketing in the name, or analyst hint"),
    ("Agencies and recruiters", "Travel management and travel agencies",
     r"^(Navan|Winmaxi Tours|Hahn Air)", 4, "travel platform, travel agency or ticketing airline"),

    ("Insurers and benefits", "Health, life and general insurers",
     r"^(Aetna|Agram Life|Care Health Insurance|Bupa|Cigna|Icici Lombard|Cici Prudential)", 8,
     "insurer brands; osiguranje means insurance"),
    ("Insurers and benefits", "Workers' compensation (statutory)",
     r"^(Allianz|Icare Nsw$)", 3, "state workers' compensation schemes in Australia"),
    ("Insurers and benefits", "Brokers and benefits consultants",
     r"^(Jensten Insurance Brokers|Mercer Limited)", 2, "an insurance broker and a benefits consultant"),
    ("Insurers and benefits", "Benefit schemes and wellness",
     r"^(Pluxee|Sodexo|Benefit Systems|Green Commute Initiative|Inside Edge Novated Leasing|Doctor Anywhere|"
     r"Vitality Works)", 7,
     "meal cards, sports card, cycle-to-work, salary-packaged cars, telehealth and wellness"),
    ("Insurers and benefits", "Occupational health",
     r"Ordinacija Medicine Rada|^Ustanova Za|^Nastavni Zavod", 5,
     "occupational medicine (medicina rada) and health institutions"),

    ("Telecoms and utilities", "Telecom and internet",
     r"^(Hrvatski Telekom|Telemach|T-Mobile|Vodafone|Starhub|British Telecommunications|Inet Telecoms|Zettanet|"
     r"New Star Networks)", 9, "telecom operators and internet providers"),
    ("Telecoms and utilities", "Telephony and messaging APIs",
     r"^(Avoxi|Click Send)", 2, "cloud phone numbers and an SMS API"),
    ("Telecoms and utilities", "Electricity, city utilities and waste",
     r"^(Hep Elektra|Zagrebacki Holding|London Waste Management)", 3,
     "electricity, the city utility company and waste collection"),

    ("Plausibly a customer or customer-mandated", "Customer procurement entities",
     r"^Telefonica", 2,
     "Telefónica group procurement (Global Services GmbH) and e-procurement (Compras Electrónicas) entities"),
    ("Plausibly a customer or customer-mandated", "Customer-mandated supplier network",
     r"^Ariba\b", 1, "SAP Ariba charges suppliers fees when customers buy through it"),
    ("Plausibly a customer or customer-mandated", "Supplier tag in the name",
     r"Supplier", 2,
     "the tag suggests the source system holds a second record for the same company, plausibly a customer account"),

    ("Travel and hospitality paid directly", "Hotels and resorts",
     r"Hotel|Resort|Hanbury Manor|Hilton Garden|Radisson|Shilton Hospitality", 15,
     "hotel, resort or hospitality in the name"),
    ("Travel and hospitality paid directly", "Airlines and ground transport",
     r"^(Croatia Airlines|Hahn Air|Lancefield Bus Service|Galop-Prijevoz|Niva Transport)", 5,
     "airline, bus service or transport (prijevoz) in the name"),

    ("Function not evident from the name", "No function word, or only a generic one",
     r"^(Advena|Aquila Remete|Athlete Service|Backoffice Associates|Bella Operation|Boe Croatia|Bonus Opinio|"
     r"Calm Achiever|Clime India|Crossland|Del Posto|Elemental Life|Etm Concessions|Expert-Ing|Fortis Trade|"
     r"Garden City|Golden Mean|Greencell Express|Harissa|Illunis|Infodata|It London|Kilgannon & Partners|"
     r"Kosmaz Technologies|Lemia|Livingstone|Make And Grow|Meluba|Mesa Verde|Mithras Consultants|Monile|New Block|"
     r"Oladi|Potomac|Profi Bar|Retriever|Rhea|Rudan|Shoff Darby|Stillmark Zagreb|Streamlinereforms|Super Odrediste|"
     r"Tau On-Line|Tiganda|Till Trade|Treci Posao|Yellow Submarine|Zivi Napitak|Adamma Info Services|"
     r"Xenon Savjetovanje|Teb Poslovno Savjetovanje|Westbrook Advisers|4I Advisory Services|4I Management Consulting|"
     r"Obrt Sjaj Sunca)\b", 55,
     "the name says nothing about the service, or only consulting, advisory, services, trade or technologies"),
    ("Function not evident from the name", "Croatian companies the analyst hints list as unknown",
     r"^(Weking|Veniture|Nefron|Bijeli Pijesak|Smart Group Services|Tp Prime|Pingo|Ramiro|Omonia|Mosaic Concept|"
     r"Limes Plus|Orcola|Akton)\b", 13,
     "analyst hint: function unknown, most likely contractors; confirm with Finance"),
    ("Function not evident from the name", "Unnamed payee",
     r"^\(Blank\)$", 1, "the source holds the placeholder (Blank) instead of a vendor name"),
]

CATEGORY_IMPLICATIONS = {
    "Individuals and owner-named businesses": (
        "The six bare personal names go to G&A with confidence low, per the analyst hint; their descriptions can say "
        "only that the payee is an individual and the purpose is not stated. Owner-named businesses are classified by "
        "what the business does (painting events, occupational medicine), not as individuals. Obrt rows are one-person "
        "businesses: where they supply labour they belong with contractors.",
        "Payments to individuals through accounts payable are a control point (contractor status, reimbursements "
        "booked as vendor spend), not a savings line; the amount is small."),
    "Consumer or retail purchases": (
        "Retail rows split by what was bought: Apple and electronics as employee IT equipment (G&A), groceries and "
        "office supplies (Facilities), restaurants and food delivery (G&A, travel and entertainment), gifts (G&A), "
        "gyms and sports cards (G&A, benefits). No streaming or consumer media subscriptions appear in the file.",
        "Many small rows and little money: the fix is a purchasing-card and expense policy, not a vendor negotiation. "
        "It belongs in the memo as one line on tail spend, if at all."),
    "Government, tax, court and regulator payees": (
        "Tax, government, regulator and statutory-scheme payees are non-discretionary: Optimize with the rationale "
        "\"non-discretionary, excluded from the savings base\"; ICO is data-protection registration (Legal). Two "
        "subgroups are not statutory despite public ownership: the student centres invoice student work, which is a "
        "labour decision, and the publicly owned utilities are ordinary utility bills (Facilities). No court payees appear.",
        "Only the statutory payees leave the savings base (total in section 10). Two items need an explanation from "
        "Finance: the City of Zagreb spatial planning office payment (large for a tenant) and the Cayman Islands "
        "Government payment (it implies a Cayman entity in the group structure)."),
    "Memberships and associations": (
        "TM Forum goes to Marketing (industry membership, per the taxonomy rules); clubs go with team events and perks; "
        "individual learning memberships go to training.",
        "TM Forum is the only material membership; everything else is tail spend. Whether TM Forum has a commercial "
        "justification depends on how much revenue comes from telecom customers."),
    "Agencies and recruiters": (
        "Recruiters, job boards and payroll or employer-of-record providers go to G&A; marketing, PR and event agencies "
        "go to Marketing; travel management to G&A.",
        "Recruiting and HR outsourcing is a Terminate candidate once the parent's talent and payroll functions take over; "
        "marketing agencies are a Consolidate candidate."),
    "Insurers and benefits": (
        "All G&A. Workers' compensation and occupational health are statutory, so they are non-discretionary.",
        "Insurance spreads across several insurers in several countries plus a broker: the Consolidate case is moving "
        "these under the parent's group programme and re-broking."),
    "Telecoms and utilities": (
        "Lines and mobile plans go to Facilities; telephony that serves support lines to Support; SMS and phone APIs to "
        "Engineering, per the taxonomy rules.",
        "Small in total; they follow office decisions rather than drive them."),
    "Plausibly a customer or customer-mandated": (
        "Telefónica and Ariba go to Sales as customer-mandated platform fees, confidence low, Optimize with the "
        "non-discretionary rationale, never Terminate. The two Supplier-tagged names are classified by what they "
        "supply (Bupa insurance, StarHub telecom), with a note that the company may also sell to them.",
        "Payments from a supplier to its customer's procurement entities are unusual. If they are rebates, credits or "
        "penalties rather than platform fees, they belong against revenue, not in vendor spend. Confirm before the memo "
        "quotes a total. Bupa and StarHub stay in the savings base, but any change to them needs a commercial check."),
    "Travel and hospitality paid directly": (
        "G&A, travel and entertainment.",
        "Hotels, airlines and ground transport paid directly are travel spend the travel platform does not see; a Navan "
        "policy lever has to cover them too."),
    "Function not evident from the name": (
        "Confidence low and a description that says the function cannot be inferred from the name (CLAUDE.md rule); "
        "for the Croatian companies the analyst hint applies and the description ends with \"confirm with Finance\".",
        "A visible share of spend cannot be described from the file alone. Recommendations on these payees stay "
        "provisional until Finance identifies them, and the memo should say so."),
}


# ---------------------------------------------------------------- small helpers

def decimals(x: float) -> int:
    d = Decimal(str(round(x, 9))).normalize()
    return max(0, -d.as_tuple().exponent)


def digit_at(x: float, place: int) -> int:
    return int(round(x * 10 ** place)) % 10


def poisson_at_least(k: int, lam: float) -> float:
    return 1.0 - sum(math.exp(-lam) * lam ** i / math.factorial(i) for i in range(k))


def chi2_sf_even(x: float, df: int) -> float:
    """Survival function of the chi-square distribution for even df (closed form)."""
    assert df % 2 == 0
    h = x / 2.0
    return math.exp(-h) * sum(h ** i / math.factorial(i) for i in range(df // 2))


def pairs_within(values_sorted: list[float], t: float) -> int:
    n = 0
    for i, x in enumerate(values_sorted):
        n += bisect.bisect_right(values_sorted, x + t, lo=i + 1) - (i + 1)
    return n


def sorted_runs(recs: list[dict]) -> list[list[dict]]:
    runs, start = [], 0
    for i in range(1, len(recs)):
        if recs[i]["cost"] > recs[i - 1]["cost"]:
            runs.append(recs[start:i])
            start = i
    runs.append(recs[start:])
    return runs


def outside_longest_sorted(recs: list[dict]) -> list[dict]:
    """Rows not in one longest non-increasing run of costs (in sheet order)."""
    seq = [-r["cost"] for r in recs]
    tails, tails_idx, prev = [], [], [-1] * len(seq)
    for i, v in enumerate(seq):
        k = bisect.bisect_right(tails, v)
        if k == len(tails):
            tails.append(v)
            tails_idx.append(i)
        else:
            tails[k] = v
            tails_idx[k] = i
        prev[i] = tails_idx[k - 1] if k else -1
    keep, i = set(), tails_idx[-1]
    while i != -1:
        keep.add(i)
        i = prev[i]
    return [recs[i] for i in range(len(recs)) if i not in keep]


def ordinal(n: int) -> str:
    words = {1: "first", 2: "second", 3: "third", 4: "fourth", 5: "fifth", 6: "sixth", 7: "seventh", 8: "eighth",
             9: "ninth", 10: "tenth"}
    return words.get(n, f"number {n}")


def unique_total(flags: list[dict], subgroups) -> tuple[int, float]:
    u = {fl["vendor_id"]: fl for fl in flags if fl["subgroup"] in subgroups}
    return len(u), sum(fl["cost"] for fl in u.values())


def lab(r: dict) -> str:
    return f"{r['vendor_id']} {r['name_fixed']}"


def lab_cost(r: dict) -> str:
    return f"{lab(r)} ({money(r['cost'])})"


def span(coords: list[str]) -> str:
    if not coords:
        return "none"
    if len(coords) == 1:
        return coords[0]
    rows = {re.sub(r"[A-Z]+", "", c) for c in coords}
    return f"{coords[0]}:{coords[-1]}" if len(rows) == 1 else ", ".join(coords)


# ---------------------------------------------------------------- analyses

def cost_analysis(recs: list[dict]) -> dict:
    costs = [r["cost"] for r in recs]
    n = len(costs)
    total = sum(costs)
    vs = sorted(costs)

    groups = defaultdict(list)
    for r in recs:
        groups[r["cost"]].append(r)
    ties = sorted((g for g in groups.values() if len(g) > 1), key=lambda g: g[0]["row"])
    cent_groups = defaultdict(list)
    for r in recs:
        cent_groups[round(r["cost"], 2)].append(r)
    cent_ties = [g for g in cent_groups.values() if len(g) > 1]
    assert sorted(sorted(x["row"] for x in g) for g in cent_ties) == sorted(sorted(x["row"] for x in g) for g in ties), \
        "cent-level and exact ties differ"
    adjacent = all(max(x["row"] for x in g) - min(x["row"] for x in g) == len(g) - 1 for g in ties)

    runs = sorted_runs(recs)
    run_info = []
    for run in runs:
        decs = Counter(decimals(r["cost"]) for r in run)
        seventh = {digit_at(r["cost"], 7) for r in run}
        if max(decs) <= 7 and seventh <= {0, 2, 4, 6, 8}:
            sig = "always even (0, 2, 4, 6 or 8)"
        elif max(decs) <= 7 and seventh <= {0, 5}:
            sig = "always 0 or 5"
        else:
            sig = "any digit"
        run_info.append({
            "first": run[0]["row"], "last": run[-1]["row"], "n": len(run),
            "hi": run[0]["cost"], "lo": run[-1]["cost"],
            "decs": decs, "sig": sig,
            "ties": sum(1 for g in ties if run[0]["row"] <= g[0]["row"] <= run[-1]["row"]),
            "tie_rows": sum(len(g) for g in ties if run[0]["row"] <= g[0]["row"] <= run[-1]["row"]),
        })

    whole_dollar = sum(1 for c in costs if abs(c - round(c)) < 1e-6)
    whole_cent = sum(1 for c in costs if abs(c * 100 - round(c * 100)) < 1e-6)
    over100 = [r for r in recs if r["cost"] >= 100]
    near100 = [r for r in over100 if abs(r["cost"] - 100 * round(r["cost"] / 100)) < 0.5]
    lam100 = len(over100) * (1.0 / 100)  # a 1-dollar window out of every 100 dollars
    over1000 = [r for r in recs if r["cost"] >= 1000]
    near1000 = [r for r in over1000 if abs(r["cost"] - 1000 * round(r["cost"] / 1000)) < 5]
    lam1000 = len(over1000) * (10.0 / 1000)

    first = Counter(int(f"{c:e}"[0]) for c in costs)
    benford, chi2, mad = [], 0.0, 0.0
    for d in range(1, 10):
        e = math.log10(1 + 1 / d)
        o = first[d] / n
        chi2 += (first[d] - n * e) ** 2 / (n * e)
        mad += abs(o - e) / 9
        benford.append((d, first[d], o, e))
    band = next(label for limit, label in NIGRINI_FIRST_DIGIT if mad <= limit)

    return {
        "n": n, "total": total, "ties": ties, "adjacent": adjacent,
        "tie_rows": sum(len(g) for g in ties), "max_tie": max((g[0]["cost"] for g in ties), default=0.0),
        "pairs_cent": pairs_within(vs, 0.005), "pairs_half": pairs_within(vs, 0.5), "pairs_dollar": pairs_within(vs, 1.0),
        "decs_all": Counter(decimals(c) for c in costs), "runs": run_info,
        "outside_sorted": outside_longest_sorted(recs),
        "whole_dollar": whole_dollar, "whole_cent": whole_cent,
        "near100": near100, "over100": len(over100), "lam100": lam100, "p100": poisson_at_least(len(near100), lam100),
        "near1000": near1000, "over1000": len(over1000), "lam1000": lam1000,
        "benford": benford, "chi2": chi2, "chi2_p": chi2_sf_even(chi2, 8), "mad": mad, "band": band,
    }


def name_analysis(recs: list[dict]) -> dict:
    named = [{"name": r["name"], "row": r["row"], "cost": r["cost"]} for r in recs]
    cand = near_duplicate_candidates(named)
    norm = cand["norm"]
    candidates = []
    for k, v in sorted(cand["norm_dups"].items(), key=lambda kv: min(x["row"] for x in kv[1])):
        candidates.append(("1: same key", {x["row"] for x in v}))
    for m in cand["near"]:
        candidates.append((f"2: {m['rule']}", {x["row"] for x in norm[m["a"]] + norm[m["b"]]}))
    for t, ks in cand["weak"]:
        candidates.append((f"3: same first token `{t}`", {x["row"] for k in ks for x in norm[k]}))
    reviewed, missing = [], []
    for tier, rows in candidates:
        try:
            verdict, reason = verdict_for(rows)
            reviewed.append((tier, rows, verdict, reason))
        except KeyError:
            missing.append(rows)
    if missing:
        raise SystemExit(f"near-duplicate candidates without a recorded verdict: {missing}")
    def found_by_search(group_rows: list[int]) -> bool:
        g = set(group_rows)
        return any(len(rows) >= 2 and rows <= g for _, rows, _, _ in reviewed)

    return {"cand": cand, "reviewed": reviewed,
            "knowledge_merges": [g for g in MERGE_GROUPS if not found_by_search(g["rows"])],
            "knowledge_links": [g for g in LINK_GROUPS if not found_by_search(g["rows"])]}


def apply_flags(recs: list[dict]) -> list[dict]:
    flags = []
    for category, subgroup, pattern, expected, evidence in FLAG_RULES:
        rx = re.compile(pattern, re.IGNORECASE)
        hits = [r for r in recs if rx.search(strip_accents(r["name_fixed"]))]
        if len(hits) != expected:
            raise SystemExit(f"flag '{subgroup}' matched {len(hits)} rows, expected {expected}: "
                             + "; ".join(r["name_fixed"] for r in hits))
        for r in hits:
            flags.append({"vendor_id": r["vendor_id"], "row": r["row"], "name_raw": r["name"],
                          "name_fixed": r["name_fixed"], "cost": r["cost"],
                          "category": category, "subgroup": subgroup, "evidence": evidence})
    return flags


# ---------------------------------------------------------------- rendering

def structure_section(f: dict) -> list[str]:
    sheets = f["sheets"]
    m = main_sheet(f)
    hidden = [s["title"] for s in sheets if s["state"] != "visible" or s["raw_state"] != "visible"]
    white = [f"`{s['title']}` {span([c for c, _ in s['white_font']])}" for s in sheets if s["white_font"]]
    white_fills = sorted({str(fill) for s in sheets for _, fill in s["white_font"]})
    invisible = sum(len(s["invisible"]) for s in sheets)
    hidden_fmt = sum(len(s["hidden_numfmt"]) for s in sheets)
    min_font = min((s["min_font"] for s in sheets if s["min_font"] is not None), default=None)
    dv = m["dvs"][0] if m["dvs"] else None
    dv_cols = {get_column_letter(c) for c in m["dv_cols"]}
    no_dv = [get_column_letter(c) for c in range(1, m["max_col"] + 1) if get_column_letter(c) not in dv_cols]
    dv_text = (f"B: list from `{dv['formula1']}`, blanks allowed, error alert on" if dv else "none")
    hyperlinks = [(s["title"], c, t) for s in sheets for c, t in s["hyperlinks"]]
    sheet_format = m["sheet_format"][0] if m["sheet_format"] else ""
    gs = (not f["docprops"]) and 'defaultColWidth="12.63"' in sheet_format and 'defaultRowHeight="15.75"' in sheet_format
    rows = [
        ["Hidden or very hidden sheets",
         f"none; {len(sheets)} of {len(sheets)} visible in openpyxl and workbook.xml" if not hidden else ", ".join(hidden),
         "nothing hidden to recover"],
        ["Hidden rows and columns",
         f"none on any sheet; no zero-height rows, zero-width columns or outline groups; AutoFilter `{m['autofilter']}` "
         f"has {m['filter_columns']} criteria",
         f"all {m['last_row'] - 1} vendor rows are visible; the row count is complete for this file"],
        ["Cell notes and comments",
         f"{sum(s['comments'] for s in sheets)} notes; {len(f['comment_parts'])} comment parts; persons list "
         f"{'empty' if not f['persons_listed'] else str(f['persons_listed'])}",
         "no reviewer context to use"],
        ["Defined names",
         f"{len(f['user_defined_names'])} user-defined; built-in only: "
         + ", ".join(f"`{d['name']}` (hidden, {d['ref']})" for d in f["builtin_names"]),
         "no named range feeds a hidden calculation"],
        ["Conditional formats",
         f"{sum(s['cf_rules'] for s in sheets)} rules; {sum(s['raw_cf'] for s in sheets)} in the XML, extension list included",
         "no colour-coded flags to interpret"],
        ["White-on-white or hidden text",
         f"{invisible} cells; white text only in header cells (" + "; ".join(white) + "), all on fill "
         + ", ".join(white_fills) + (" (dark blue)" if white_fills == ["FF073763"] else "")
         + f"; {hidden_fmt} cells with a `;;;` format; smallest font {min_font:g} pt",
         "no hidden content"],
        ["Data validation, column by column",
         f"{dv_text}; none on {', '.join(no_dv)}; {sum(s['raw_x14_dv'] for s in sheets)} x14 extension rules; "
         f"no rules on the other {len(sheets) - 1} sheets",
         "Department values must match `Config` character for character; Description and Suggestions are free text"],
        [f"Columns {get_column_letter(m['last_col'] + 1)} to {get_column_letter(m['max_col'])} and rows "
         f"{m['last_row'] + 1} to {m['max_row']}",
         f"no values, formulas, comments, hyperlinks or merged cells; {m['styled_beyond_cols']:,} and "
         f"{m['styled_beyond_rows']:,} cells carry styles only (borders, fonts, number formats)",
         f"nothing outside {data_range(m)} to analyse"],
        ["Formulas", f"{sum(s['formulas'] for s in sheets)} in the workbook", "every cost is a typed value, not a calculation"],
        ["Other objects",
         f"{len(hyperlinks)} hyperlink ("
         + "; ".join(f"{c} to {t}" for _, c, t in hyperlinks)
         + f"); {sum(s['images'] for s in sheets)} images; {sum(s['charts'] for s in sheets)} charts; "
         f"{len(f['drawing_parts'])} drawing parts, {len(f['drawings_with_content'])} with content; "
         f"{sum(s['merged'] for s in sheets)} merged cells; sheet protection on {sum(1 for s in sheets if s['protected'])} sheets",
         "harmless; the link is the cell's own text"],
        ["Shared strings",
         f"{f['shared_strings']} strings, {f['shared_strings_unreferenced']} not used by any cell",
         "no leftover text from deleted cells"],
        ["Package contents",
         f"macros {len(f['macros'])}, external links {len(f['external_links'])}, pivot caches {len(f['pivots'])}, "
         f"embedded objects {len(f['embeddings'])}, custom XML {len(f['custom_xml'])}, document properties "
         f"{len(f['docprops'])}",
         "no external dependencies; author and dates are not recorded in the file"],
        ["Origin",
         "Google Sheets export: no document properties, Sheets default column width 12.63 and row height 15.75, "
         "empty drawing parts" if gs else "not identified",
         f"the {m['max_row']}-row by {m['max_col']}-column grid is a Sheets grid size; see section 8"],
    ]
    out = ["## 1. Workbook structure", "",
           "Re-verified with openpyxl and, for what openpyxl does not surface, the raw package XML. The separate "
           "structure audit is confirmed in the addendum of `00_data_profile.md`; this table adds the remaining checks.",
           ""]
    out += table(["Check", "Result", "Implication"], rows)
    return out


def ties_section(c: dict) -> list[str]:
    out = ["## 2. Identical amounts", ""]
    out.append(f"{len(c['ties'])} groups of rows share an identical cost, to the cent and in fact to every stored decimal: "
               f"{c['tie_rows']} rows in all. Every group sits on consecutive rows of the sorted sheet "
               f"({'confirmed' if c['adjacent'] else 'NOT confirmed'}), the largest amount is {money(c['max_tie'])}, and "
               "with one exception the payees in a group are unrelated (a kitchen and the Australian tax office; an SMS "
               "API, a print shop and a hospitality firm).")
    out.append("")
    rows = [[i, f"${g[0]['cost']:,.2f}", ", ".join(str(r["row"]) for r in g), "; ".join(r["name_fixed"] for r in g)]
            for i, g in enumerate(c["ties"], start=1)]
    out += table(["#", "Amount", "Rows", "Vendors"], rows)
    out.append("")
    out.append(f"Why these are not duplicate payments: {c['pairs_cent']} pairs of rows are within half a cent of each other, "
               f"and widening the window a hundredfold, to 50 cents, adds only {c['pairs_half'] - c['pairs_cent']} more. If "
               "amounts were spread continuously, near misses would outnumber exact matches by about a hundred to one. "
               "Here exact matches are almost the only close pairs, so the amounts sit on a discrete grid. That is the "
               "pattern left when amounts recorded in whole units are multiplied by a common factor: two small amounts "
               "that were equal stay equal after scaling, and the many small vendors make such collisions common. The "
               "brief says costs were modified; this is consistent with that. No attempt is made to reverse the "
               "modification, because the data owner applied it on purpose and the analysis does not need it.")
    out.append("")
    out.append("The one group that may be a genuinely identical price is the three Croatian occupational-medicine "
               "providers at $20.27 each, which plausibly charge the same fee for the statutory medical examination.")
    out.append("")
    out.append("- Implication for classification: none. Every row stays, with its own cost.")
    out.append("- Implication for the memo: the file cannot support a duplicate-payment finding either way. If the CFO "
               "wants one, it needs invoice-level data (invoice number, date, amount, payee bank account). The "
               "methodology should say the ties were tested and explained.")
    return out


def precision_section(c: dict) -> list[str]:
    out = ["## 3. Cost precision and round numbers", ""]
    out.append(f"No cost is a whole dollar ({c['whole_dollar']}) or a whole cent ({c['whole_cent']}). After rounding away "
               "binary floating-point noise, the stored precision ranges from "
               f"{min(c['decs_all'])} to {max(c['decs_all'])} decimal places: "
               + ", ".join(f"{k} places: {v}" for k, v in sorted(c["decs_all"].items())) + ".")
    out.append("")
    out.append("The precision is not random. It changes exactly where the sheet's sort order breaks (section 5):")
    out.append("")
    rows = [[f"{ri['first']} to {ri['last']}", ri["n"], f"{money(ri['hi'])} to {money(ri['lo'])}",
             ", ".join(f"{k}: {v}" for k, v in sorted(ri["decs"].items())), ri["sig"]]
            for ri in c["runs"]]
    out += table(["Rows", "Vendors", "Cost range", "Decimal places (count)", "7th decimal digit"], rows)
    out.append("")
    out.append("A 7th decimal that is always even in one block and always 0 or 5 in the next cannot come from invoices. "
               "It is the fingerprint of the modification, applied block by block with different settings. The "
               "round-versus-precise split therefore means nothing about vendors: not estimates against invoices, not "
               "currency, not accruals.")
    out.append("")
    out.append(f"Round-number check. Costs of $100 or more within 50 cents of a round hundred: {len(c['near100'])} of "
               f"{c['over100']}, against about {c['lam100']:.1f} expected by chance (Poisson probability of {len(c['near100'])} "
               f"or more: {c['p100']:.2f}). Costs of $1,000 or more within $5 of a round thousand: {len(c['near1000'])} of "
               f"{c['over1000']}, against about {c['lam1000']:.1f} expected. The first is a weak excess that may mean a "
               "handful of originals were round contract prices; it cannot be used for anything.")
    out.append("")
    out += table(["Row", "Vendor", "Cost"], [[r["row"], r["name_fixed"], f"${r['cost']:,.2f}"] for r in c["near100"]])
    out.append("")
    out.append("- Implication for classification: none.")
    out.append("- Implication for the memo: quote whole dollars or thousands, never cents; state once that the figures are "
               "the file's modified values. Shares and rankings inside the file are internally consistent, which is all "
               "the analysis needs.")
    return out


def benford_section(c: dict) -> list[str]:
    out = ["## 4. First-digit distribution", ""]
    rows = [[d, k, pct(o), pct(e), f"{100 * (o - e):+.1f} pts"] for d, k, o, e in c["benford"]]
    out += table(["First digit", "Vendors", "Observed", "Benford expectation", "Difference"], rows)
    out.append("")
    out.append(f"Chi-square {c['chi2']:.2f} on 8 degrees of freedom, p = {c['chi2_p']:.2f}; mean absolute deviation "
               f"{c['mad']:.4f}, which is {c['band']} on Nigrini's first-digit scale. The largest gap is the digit 7 "
               "(fewer vendors than expected), within what a sample of this size produces.")
    out.append("")
    out.append("Benford's law is scale-invariant, so multiplying blocks of costs by constants does not disturb it, and "
               "annual totals per vendor are sums of many invoices, which tend to conform anyway. Conformity here is "
               "therefore expected and proves little.")
    out.append("")
    out.append("- Implication for classification: none.")
    out.append("- Implication for the memo: nothing to report. Fraud or error testing needs invoice-level data.")
    return out


def order_section(c: dict) -> list[str]:
    out = ["## 5. Row order", ""]
    runs = c["runs"]
    out.append(f"The sheet looks sorted by cost, largest first, but it is {len(runs)} separately sorted blocks placed end to "
               "end. Inside each block the order is strictly non-increasing; at each boundary the cost jumps up:")
    out.append("")
    rows = []
    for a, b in zip(runs, runs[1:]):
        rows.append([f"{a['last']} to {b['first']}", money(a["lo"]), money(b["hi"])])
    out += table(["Boundary (rows)", "Last cost of the block above", "First cost of the block below"], rows)
    out.append("")
    oos = c["outside_sorted"]
    out.append(f"Removing {len(oos)} rows would make the whole sheet sorted (rows "
               + ", ".join(str(r["row"]) for r in oos) + "). They are the rows where neighbouring blocks overlap in value "
               "at the two boundaries, which is what joining separately sorted blocks produces; nothing points to rows "
               "edited one by one. The boundaries coincide with the precision changes in section 3, so the blocks are "
               "where the modification settings changed.")
    out.append("")
    out.append("- Implication for classification: none.")
    out.append("- Implication for the memo: rank vendors by cost, never by row number; near the two boundaries a vendor "
               "on a lower row can cost more than one above it.")
    return out


def names_section(na: dict, recs_by_row: dict) -> list[str]:
    cand = na["cand"]
    out = ["## 6. Near-duplicate names", ""]
    out.append("Method: the matching key from `00_data_profile.md` (mojibake repaired, accents stripped, lower case, "
               "legal forms, geography, stop words and the Supplier tag removed), searched in three tiers. Tier 1: same key "
               f"({len(cand['norm_dups'])} groups). Tier 2: similar spelling, a token subset, or two shared tokens covering "
               f"half the shorter key ({len(cand['near'])} pairs). Tier 3: same first token where a pair was not already "
               f"flagged ({len(cand['weak'])} groups). Every candidate has a recorded verdict; the script stops if one does "
               "not.")
    out.append("")
    out.append("Merge policy (decision of 2026-11-10, `docs/decisions.md`): merge only when it is the same vendor "
               "relationship under a changed or variant name (a rename, a spelling variant, the same contract moved between "
               "entities). Where entities share a parent or brand but supply different products or contracts, or share a "
               "lineage, record a link instead: linked vendors stay separate.")
    out.append("")

    def names(rows):
        return "; ".join(f"{r} {recs_by_row[r]['name_fixed']}" for r in sorted(rows))

    def spend(rows):
        return sum(recs_by_row[x]["cost"] for x in rows)

    rows = [[tier, names(r), verdict, reason] for tier, r, verdict, reason in na["reviewed"]]
    out += table(["Tier", "Rows and names", "Verdict", "Reason"], rows)
    out.append("")
    out.append("Merges and links that string matching cannot find, from knowledge of the vendors:")
    out.append("")
    rows = [[names(g["rows"]), f"{g['status']} into {g['canonical']}", g["reason"]] for g in na["knowledge_merges"]]
    rows += [[names(g["rows"]), f"link: {g['label']} ({g['type']})", g["reason"]] for g in na["knowledge_links"]]
    out += table(["Rows and names", "Treatment", "Reason"], rows)
    out.append("")
    n = len(recs_by_row)
    merged_rows = sum(len(g["rows"]) for g in MERGE_GROUPS)
    proposed = [g for g in MERGE_GROUPS if g["status"] != "merge"]
    vendors = n - merged_rows + len(MERGE_GROUPS)
    vendors_if_reversed = vendors + sum(len(g["rows"]) - 1 for g in proposed)
    if proposed:
        out.append(f"Result: {len(MERGE_GROUPS) - len(proposed)} merges and {len(proposed)} proposed merge cover "
                   f"{merged_rows} rows, so {n} rows become {vendors} vendors ({vendors_if_reversed} if the proposed merge "
                   "is reversed):")
    else:
        out.append(f"Result: {len(MERGE_GROUPS)} merges cover {merged_rows} rows, so {n} rows become {vendors} vendors. "
                   "The 4i merge and the Sodexo SVC India rename to Pluxee India were settled by web verification in "
                   "step 3 (`docs/decisions.md`):")
    out.append("")
    out += table(["Vendor after merge", "Rows", "Combined 12-month cost", "Status", "Confidence"],
                 [[g["canonical"], ", ".join(map(str, g["rows"])), money(spend(g["rows"])), g["status"], g["confidence"]]
                  for g in sorted(MERGE_GROUPS, key=lambda g: -spend(g["rows"]))])
    out.append("")
    out.append(f"{len(LINK_GROUPS)} link groups keep their vendors separate. Their combined spend is shown because a "
               "negotiation can cover the whole group; it is not added to any one vendor:")
    out.append("")
    out += table(["Link group", "Type", "Recommendation", "Rows", "Combined 12-month cost"],
                 [[g["label"], g["type"], g["recommendation"], ", ".join(map(str, g["rows"])), money(spend(g["rows"]))]
                  for g in sorted(LINK_GROUPS, key=lambda g: -spend(g["rows"]))])
    out.append("")
    out.append(f"- Implication for classification: the sheet is filled per row, so all {n} rows get their own department, "
               "description and recommendation (`docs/decisions.md`, steps 2c and 2d). Merges and links serve only "
               "ranking and savings roll-ups. The rows of a merge group, and of a link group of the same kind of service, "
               "carry one recommendation (Slack inside the Salesforce renewal, one Bupa relationship across countries)"
               + ("; a proposed merge counts as a group until web verification confirms or reverses it" if proposed else "")
               + ". Link groups whose rows are different services ("
               + " and ".join(g["label"] for g in LINK_GROUPS if g["recommendation"] != "shared")
               + ") take a recommendation per row. Every grouped row's rationale names its group. Same-type vendors that "
               "are neither merged nor linked (student centres, clinics, hotels, corporate secretaries) are consolidation "
               "questions for the classification step.")
    link_spend = {g["label"]: spend(g["rows"]) for g in LINK_GROUPS}
    out.append(f"- Implication for the memo: the vendor count is {vendors}"
               + (f" ({vendors_if_reversed} if the proposed merge is reversed)" if proposed else "")
               + f", not {n}. Navan, already second, grows from {money(recs_by_row[3]['cost'])} to "
               f"{money(spend([3, 24]))} across its old and new names. A linked group can be quoted as one figure where "
               f"one negotiation covers it (Telefónica {money(link_spend['Telefónica'])}, HR Solution International "
               f"{money(link_spend['HR Solution International'])}), but its vendors stay separate rows.")
    return out


def flags_section(flags: list[dict], total: float) -> list[str]:
    out = ["## 7. Payee types", "",
           "Flags describe what a vendor's name shows; they are not departments, and a vendor can carry several. "
           "Each subgroup is a pattern with an expected match count that the script checks. Full list, one row per vendor "
           f"and flag: `{rel(OUT_CSV)}`.", ""]
    by_cat: dict[str, list[dict]] = defaultdict(list)
    for fl in flags:
        by_cat[fl["category"]].append(fl)
    order = list(dict.fromkeys(rule[0] for rule in FLAG_RULES))
    for i, cat in enumerate(order, start=1):
        items = by_cat[cat]
        unique = {fl["vendor_id"]: fl for fl in items}
        cat_total = sum(fl["cost"] for fl in unique.values())
        out.append(f"### 7.{i} {cat}")
        out.append("")
        out.append(f"{len(unique)} vendors, {money(cat_total)} ({pct(cat_total / total)} of spend).")
        out.append("")
        rows = []
        for sub in dict.fromkeys(fl["subgroup"] for fl in items):
            members = sorted((fl for fl in items if fl["subgroup"] == sub), key=lambda fl: -fl["cost"])
            rows.append([sub, len(members), money(sum(m["cost"] for m in members)), members[0]["evidence"],
                         "; ".join(f"{m['vendor_id']} {m['name_fixed']} ({money(m['cost'])})" for m in members)])
        out += table(["Subgroup", "Vendors", "Spend", "Evidence", "Vendors (largest first)"], rows)
        out.append("")
        if cat == "Consumer or retail purchases":
            out.append("Streaming and consumer media subscriptions: none found (no Netflix, Spotify, Disney, YouTube, "
                       "Apple TV or similar names).")
            out.append("")
        if cat == "Government, tax, court and regulator payees":
            out.append("Courts: none found.")
            out.append("")
        cls, memo = CATEGORY_IMPLICATIONS[cat]
        out.append(f"- Implication for classification: {cls}")
        out.append(f"- Implication for the memo: {memo}")
        out.append("")
    return out


def suspicious_section(recs: list[dict], c: dict, flags: list[dict], f: dict) -> list[str]:
    by_row = {r["row"]: r for r in recs}
    total = c["total"]
    costs_desc = sorted((r["cost"] for r in recs), reverse=True)
    sf = by_row[2]
    assert sf["name"].startswith("Salesforce")
    merged_cost: dict[str, float] = {}
    for g in MERGE_GROUPS:
        merged_cost[g["canonical"]] = sum(by_row[x]["cost"] for x in g["rows"])
    in_group = {x for g in MERGE_GROUPS for x in g["rows"]}
    canon = sorted([v for v in merged_cost.values()] + [r["cost"] for r in recs if r["row"] not in in_group], reverse=True)
    second = canon[1]
    run_sum, k = 0.0, 0
    for v in canon[1:]:
        if run_sum + v > sf["cost"]:
            break
        run_sum += v
        k += 1
    weking = by_row[9]
    assert weking["name"].startswith("Weking")
    weking_rank = costs_desc.index(weking["cost"]) + 1
    unknown = {fl["vendor_id"]: fl for fl in flags if fl["category"] == "Function not evident from the name"}
    unknown_total = sum(fl["cost"] for fl in unknown.values())
    unknown_material = sorted((fl for fl in unknown.values() if fl["cost"] >= MATERIAL), key=lambda fl: -fl["cost"])
    hinted = {fl["vendor_id"]: fl for fl in flags if fl["subgroup"] == "Croatian companies the analyst hints list as unknown"}
    tel = sum(by_row[x]["cost"] for x in (15, 93))
    gz, cay, ato = by_row[73], by_row[361], by_row[333]
    bb, pink = by_row[223], by_row[162]
    assert bb["name"].startswith("Bb Football") and pink["name"].startswith("Pink Ribbon")
    m = main_sheet(f)
    direct_te = {fl["vendor_id"]: fl for fl in flags if fl["category"] == "Travel and hospitality paid directly"}
    food = {fl["vendor_id"]: fl for fl in flags
            if fl["subgroup"] == "Restaurants, cafes, bakeries, caterers and food delivery"}
    small_retail = {fl["vendor_id"]: fl for fl in flags
                    if fl["category"] == "Consumer or retail purchases" and fl["cost"] < SMALL}
    out = ["## 8. Suspicious or unexplained", ""]
    items = [
        ("Salesforce is 39.5% of all spend",
         f"{lab_cost(sf)} is {pct(sf['cost'] / total)} of the total, {sf['cost'] / second:.1f} times the next vendor "
         f"after merging, and more than the next {k} vendors combined. The file does not say whether this is CRM "
         "licences for staff, platform or OEM fees tied to the company's own product, or a multi-year prepayment.",
         "The savings lever depends entirely on which it is; no Salesforce saving should be sized before the contract "
         "is read."),
        ("The eighth largest vendor cannot be identified",
         f"{lab_cost(weking)} ranks {ordinal(weking_rank)} by cost and its name says nothing about its service. With the other "
         f"hinted Croatian companies, {len(hinted)} payees total {money(sum(x['cost'] for x in hinted.values()))}; all "
         f"payees whose function the name does not show total {money(unknown_total)} ({pct(unknown_total / total)}).",
         "Finance has to identify these before the memo relies on them; one-person Croatian companies supplying labour "
         "also carry an employment-status question."),
        ("A supplier paying its customer's procurement entities",
         f"Telefónica Global Services GmbH and Telefónica Compras Electrónicas S.L. receive {money(tel)}. "
         "These are Telefónica's purchasing entities, so the company is most likely a Telefónica supplier.",
         "Platform fees are a cost of selling; rebates, credits or penalties are revenue items booked as vendor spend. "
         "Either way they are not discretionary."),
        ("Two names carry a Supplier tag",
         "`Bupa- Supplier` and `Starhub Ltd (Supplier)`. A tag like this usually separates a vendor record from another "
         "record of the same company.",
         "If StarHub or Bupa are also customers, terminating or re-tendering them is a commercial decision, not a "
         "procurement one."),
        ("A large municipal planning payment",
         f"{lab_cost(gz)}: the City of Zagreb's office for spatial planning. Fees of this size usually relate to permits "
         "or building works, which a tenant rarely pays.",
         "Likely one-off and non-discretionary; ask Finance what it was for."),
        ("Government payees that point at the group structure",
         f"{lab_cost(cay)} implies a Cayman Islands entity; {lab_cost(ato)} is tax paid through accounts payable.",
         "Confirm the legal-entity map with the parent; tax payments are not vendor spend."),
        ("Payees whose purpose is unclear",
         f"{lab_cost(bb)} (a football scouting company) and {lab_cost(pink)} (a shop).",
         "Small, but they are the kind of line a CFO asks about; classify with confidence low."),
        ("Card and expense transactions in an accounts-payable list",
         f"`Uber *Eats` is a card-statement descriptor; {len(small_retail)} retail rows are under {money(SMALL)}; "
         f"{len(food)} food and drink payees are paid as vendors; {len(direct_te)} hotels, airlines and transport "
         "companies are paid directly rather than through Navan.",
         "The vendor count overstates the supplier base; tail spend is a policy question (cards, expenses, Navan), not "
         "a negotiation."),
        ("The same vendor under old and new names",
         "Navan is paid as `Navan (Tripactions Inc)` and `Navan, Inc`. Sodexo SVC India and Pluxee India also appear "
         "side by side; web verification in step 3 showed that Sodexo SVC India is Pluxee India's former legal name, "
         "the meal-card business renamed in 2024, so they are one relationship as well.",
         "The vendor master was not cleaned after either rename; each pair is merged (section 6) and its recommendation "
         "names one entity."),
        ("Grid size and dropdown source",
         f"The vendor sheet's grid runs to row {m['max_row']} and the Department dropdown reads `Config` rows 2 to 814, "
         f"although the data ends at row {m['last_row']} and `Config` at row 13.",
         "Consistent with a template or an earlier, longer version of the sheet. Nothing in the file shows whether the "
         f"{m['last_row'] - 1} rows are every vendor paid in the 12 months; the memo should call the total the spend in "
         "this file."),
        ("Name damage beyond mojibake",
         "`Magazin Raunalni Sistemi` has lost the letter č (Računalni, computer); `Cici Prudential` is ICICI "
         "Prudential without its first letter; `Mcburneys Charted Accountants` misspells Chartered.",
         "The cleaning step repairs a display name only where the correct form is certain (the č); the others are "
         "noted, not rewritten."),
        ("Explained, not suspicious",
         f"Identical amounts (section 2), the precision pattern (section 3) and the row-order breaks (section 5) are all "
         "consequences of the cost modification; the first-digit test (section 4) shows nothing unusual.",
         "Mention once in the methodology; nothing for the memo."),
    ]
    for i, (title, what, implication) in enumerate(items, start=1):
        out.append(f"{i}. **{title}.** {what} Implication: {implication}")
    out.append("")
    if unknown_material:
        out.append(f"Payees over {money(MATERIAL)} whose function the name does not show:")
        out.append("")
        out += table(["Vendor", "12-month cost", "Flag"],
                     [[f"{fl['vendor_id']} {fl['name_fixed']}", money(fl["cost"]), fl["subgroup"]] for fl in unknown_material])
    return out


def rollup_sections(c: dict, flags: list[dict], total: float) -> list[str]:
    def cat_total(cat):
        u = {fl["vendor_id"]: fl for fl in flags if fl["category"] == cat}
        return len(u), sum(fl["cost"] for fl in u.values())

    stat_n, stat_t = unique_total(flags, STATUTORY_SUBGROUPS)
    cm_n, cm_t = unique_total(flags, CUSTOMER_MANDATED_SUBGROUPS)
    ins_n, ins_t = cat_total("Insurers and benefits")
    unk_n, unk_t = cat_total("Function not evident from the name")
    agency = {fl["vendor_id"]: fl for fl in flags if fl["subgroup"] in (
        "Recruitment agencies", "Job boards and recruiting platforms", "Employer of record, payroll and HR outsourcing")}
    out = ["## 9. What this means for classification", ""]
    out += [
        f"- Classify all {c['n']} rows, each with its own department, description and recommendation. Rows in one of the "
        f"{len(MERGE_GROUPS)} merge groups"
        + (f" ({sum(1 for g in MERGE_GROUPS if g['status'] != 'merge')} of them proposed)"
           if any(g["status"] != "merge" for g in MERGE_GROUPS) else "") + " or one of the "
        f"{sum(1 for g in LINK_GROUPS if g['recommendation'] == 'shared')} link groups marked shared carry the same "
        f"recommendation; the {sum(1 for g in LINK_GROUPS if g['recommendation'] != 'shared')} link groups of different "
        "services take one per row; every grouped row's rationale names its group. Merges and links otherwise serve only "
        "ranking and savings roll-ups.",
        f"- Set confidence low for the {unk_n} payees whose function the name does not show and for the six individuals; "
        "say so in the description rather than guessing.",
        "- Use the Croatian glossary terms surfaced here (obrt, vl., grad, osiguranje, medicina rada, prijevoz, dostava, "
        "ugostiteljstvo, savjetovanje, udruga) so Croatian descriptions are translations.",
        "- Statutory, government and customer-mandated payees take Optimize with the non-discretionary rationale.",
        "- Departments must match `Config` exactly; the dropdown enforces it in the workbook and the QA script will too.",
        "",
        "## 10. What this means for the memo",
        "",
        f"- Excluded from the savings base: {stat_n} statutory payees (tax, government, regulators, workers' "
        f"compensation, occupational health) at {money(stat_t)}, and {cm_n} customer-mandated payees (Telefónica, "
        f"Ariba) at {money(cm_t)}, pending Finance's answer on Telefónica: {money(stat_t + cm_t)} in all. Student "
        "centres, utilities and the Supplier-tagged names stay in the base.",
        f"- Provisional: {money(unk_t)} ({pct(unk_t / total)}) sits with payees the file does not identify.",
        f"- Candidate themes the forensic pass supports: insurance and benefits across {ins_n} payees "
        f"({money(ins_t)}); recruiting and HR outsourcing ({money(sum(fl['cost'] for fl in agency.values()))}); Navan as "
        "one vendor; Salesforce once its contract nature is known.",
        "- Present money in whole dollars or thousands, call the total the spend in this file, and say once that costs "
        "were modified by the data owner.",
    ]
    return out


def summary_section(f: dict, c: dict, na: dict, flags: list[dict], recs: list[dict]) -> list[str]:
    total = c["total"]
    by_row = {r["row"]: r for r in recs}
    merge_rows = sum(len(g["rows"]) for g in MERGE_GROUPS)
    proposed = sum(1 for g in MERGE_GROUPS if g["status"] != "merge")
    navan = sum(by_row[x]["cost"] for x in (3, 24))

    def cat(catname):
        u = {fl["vendor_id"]: fl for fl in flags if fl["category"] == catname}
        return len(u), sum(fl["cost"] for fl in u.values())

    unk_n, unk_t = cat("Function not evident from the name")
    cons_n, cons_t = cat("Consumer or retail purchases")
    cm_n, cm_t = unique_total(flags, CUSTOMER_MANDATED_SUBGROUPS)
    stat_n, stat_t = unique_total(flags, STATUTORY_SUBGROUPS)
    m = main_sheet(f)
    return [
        "## Summary",
        "",
        f"- **Structure is clean.** Nothing hidden, no comments, no conditional formats, no formulas, nothing outside "
        f"{data_range(m)}; the only validation is the Department dropdown. One hidden built-in name exists for the "
        "AutoFilter. Section 1.",
        f"- **Identical amounts are not duplicate payments.** {len(c['ties'])} groups ({c['tie_rows']} rows) share a cost to "
        f"every decimal, but they are unrelated payees on adjacent rows, the largest {money(c['max_tie'])}, and the "
        "amounts sit on a discrete grid left by the cost modification. Section 2.",
        f"- **Decimals mean nothing.** No round numbers at all; precision changes block by block with the cost "
        "modification. Quote whole dollars. Section 3.",
        f"- **First digits conform** to Benford's law ({c['band']}, p = {c['chi2_p']:.2f}). Section 4.",
        f"- **Row order is not a rank.** The sheet is {len(c['runs'])} sorted blocks end to end. Section 5.",
        f"- **{len(MERGE_GROUPS) - proposed} merges"
        + (f" and {proposed} proposed merge" if proposed else "") + f"** ({merge_rows} rows) give "
        f"{len(recs) - merge_rows + len(MERGE_GROUPS)} vendors; Navan, already second, grows to {money(navan)} across its "
        f"old and new names. {len(LINK_GROUPS)} link groups (Slack with Salesforce, Bupa's and Apple's country entities, "
        "and others) keep their vendors separate. Section 6.",
        f"- **Customer-mandated payees:** Telefónica's two procurement entities and SAP Ariba, {money(cm_t)}. "
        "Non-discretionary; confirm what the Telefónica payments are. Bupa and StarHub carry a Supplier tag and may "
        "also be customers. Sections 7.8 and 8.",
        f"- **Savings base:** {money(stat_t + cm_t)} of statutory and customer-mandated spend is excluded. Section 10.",
        f"- **Unidentified payees:** {unk_n} names, {money(unk_t)} ({pct(unk_t / total)} of spend), led by Weking d.o.o. at "
        f"{money(by_row[9]['cost'])}. Sections 7.10 and 8.",
        f"- **Consumer and retail purchases:** {cons_n} vendors, {money(cons_t)}; a card and expense policy issue, not a "
        "negotiation. Section 7.2.",
        f"- **Salesforce is {pct(by_row[2]['cost'] / total)} of spend** and the file does not say what the contract covers. "
        "Section 8.",
        "",
    ]


def flags_csv(flags: list[dict]) -> str:
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\n")
    w.writerow(["vendor_id", "source_row", "vendor_name_raw", "vendor_name_repaired", "cost_usd", "category", "subgroup",
                "evidence"])
    for fl in sorted(flags, key=lambda x: (x["row"], x["category"], x["subgroup"])):
        w.writerow([fl["vendor_id"], fl["row"], fl["name_raw"], fl["name_fixed"], repr(fl["cost"]), fl["category"],
                    fl["subgroup"], fl["evidence"]])
    return buf.getvalue()


def main() -> int:
    before = sha256(RAW_PATH)
    facts = structure_audit(RAW_PATH)
    recs = load_vendor_records(RAW_PATH)
    by_row = {r["row"]: r for r in recs}
    c = cost_analysis(recs)
    na = name_analysis(recs)
    flags = apply_flags(recs)
    after = sha256(RAW_PATH)
    if before != after:
        raise SystemExit("raw workbook changed during the run")

    lines = [
        "# Forensic pass: vendor_analysis_assessment.xlsx",
        "",
        f"Generated {date.today().isoformat()} by `scripts/01_forensics.py`. The workbook was opened read-only; its "
        f"SHA-256 was `{before}` before and after the run. Nothing is classified here: departments, descriptions and "
        f"recommendations come later. Vendor names are shown with the mojibake repaired; `vendor_id` is `V` plus the "
        f"source row number. Total spend in the file: {money(c['total'])} across {c['n']} rows.",
        "",
    ]
    lines += summary_section(facts, c, na, flags, recs)
    lines += structure_section(facts) + [""]
    lines += ties_section(c) + [""]
    lines += precision_section(c) + [""]
    lines += benford_section(c) + [""]
    lines += order_section(c) + [""]
    lines += names_section(na, by_row) + [""]
    lines += flags_section(flags, c["total"])
    lines += suspicious_section(recs, c, flags, facts) + [""]
    lines += rollup_sections(c, flags, c["total"]) + [""]
    text = "\n".join(lines)
    write_text(OUT_MD, text)
    write_text(OUT_CSV, flags_csv(flags))
    print(f"wrote {rel(OUT_MD)} ({len(text):,} chars) and {rel(OUT_CSV)} ({len(flags)} flag rows)")
    print(f"ties: {len(c['ties'])} groups / {c['tie_rows']} rows; runs: {[(r['first'], r['last']) for r in c['runs']]}; "
          f"benford: chi2={c['chi2']:.2f} p={c['chi2_p']:.3f} MAD={c['mad']:.4f}")
    print(f"name candidates reviewed: {len(na['reviewed'])}; found by knowledge: {len(na['knowledge_merges'])} merges, "
          f"{len(na['knowledge_links'])} links")
    return 0


if __name__ == "__main__":
    sys.exit(main())
