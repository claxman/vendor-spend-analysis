"""Step 3: build the input files for the web-verification agents (one line per vendor: id, cleaned name, AP name,
spend, legal-form clue, analyst hint, name note). Copied into the repository in step 5 as it ran.

Usage: python scripts/research_inputs.py <output directory>   (the files it wrote are in qa/research/inputs)
"""
import csv, re, sys
from pathlib import Path
REPO = Path(__file__).resolve().parent.parent
OUT = Path(sys.argv[1])
rows = list(csv.DictReader(open(REPO / "outputs/vendors_clean.csv", encoding="utf-8")))
hints = {}
for line in (REPO / "docs/vendor_hints.md").read_text(encoding="utf-8").split("## Notes")[0].splitlines():
    m = re.match(r"^\| (\d+) \| (.*?) \| (.*) \|$", line)
    if m:
        for vid in re.findall(r"`(V\d{4})`", m.group(3)):
            hints.setdefault(vid, []).append(f"hint {m.group(1)}: {m.group(2)}")
CLUES = [
    (r"\bj\.?d\.?o\.?o\.?|\bd\.o\.o\.|\bd\.d\.|\bobrt\b|zagreb|split\b|hrvatsk|croatia", "Croatia"),
    (r"private limited|pvt\.? ltd|\bp ltd\b|chennai|india|mahabalipuram|puducherry|adyar", "India"),
    (r"\bpty\b|australia|melbourne|\bnsw\b|\bwa\b|\baus\b", "Australia"),
    (r"\bpte\b|singapore|\bsg\b", "Singapore"),
    (r"\bgmbh\b", "Germany, Austria or Switzerland"), (r"\bag\b", "Switzerland or Germany"),
    (r"s\.r\.o\.", "Czech Republic or Slovakia"), (r"\baps\b|\ba/s\b", "Denmark"), (r"\boy\b", "Finland"),
    (r"\bbvba\b", "Belgium"), (r"\bs\.l\.", "Spain"), (r"ireland", "Ireland"),
    (r"\binc\b|\bllc\b|\bp\.c\.", "United States"),
    (r"\bltd\b|limited|\bllp\b|\bplc\b|london|manchester|\buk\b", "United Kingdom"),
]
def clue(name):
    n = name.lower()
    for pat, country in CLUES:
        if re.search(pat, n):
            return country
    return "none"
for b in range(10):
    chunk = rows[b * 40:(b + 1) * 40]
    half = (len(chunk) + 1) // 2 if b == 9 else 20
    for part, sub in (("a", chunk[:half]), ("b", chunk[half:])):
        lines = []
        for r in sub:
            fields = [r["vendor_id"], r["vendor_name_clean"], "AP name: " + r["vendor_name_raw"],
                      f"${float(r['cost_usd']):,.0f}", "legal-form clue: " + clue(r["vendor_name_clean"]),
                      " / ".join(hints.get(r["vendor_id"], [])) or "no hint"]
            if r["name_notes"]:
                fields.append("name note: " + r["name_notes"])
            lines.append(" | ".join(fields))
        (OUT / f"input_{b + 1:02d}{part}.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
        print(f"input_{b + 1:02d}{part}.txt: {len(sub)} vendors, {sub[0]['vendor_id']} to {sub[-1]['vendor_id']}")
