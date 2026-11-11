"""Step 2: build docs/vendor_hints.md from the analyst hints in prompt 6 (prompts/log.md), mapping each hint to the rows
it covers. Copied into the repository in step 5 as it ran; run from the repository root.
"""
import sys, json
from pathlib import Path
sys.path.insert(0, str(Path.cwd() / "scripts"))
from vsa_common import load_vendor_records
recs = {r["row"]: r for r in load_vendor_records()}
log = Path("prompts/log.md").read_text(encoding="utf-8")
para = next(line for line in log.splitlines() if line.startswith("Cloudcrossing BVBA:"))
H = [
 ("Cloudcrossing BVBA: Belgian Salesforce consulting partner.", [6]),
 ("Kimble Applications: PSA software on the Salesforce platform (now Kantata).", [27]),
 ("Mason Frank: Salesforce-specialist recruitment agency.", [34]),
 ("Yoxel: Salesforce email and calendar sync.", [170]),
 ("Navan (both entities): corporate travel and expense platform.", [3, 24]),
 ("TOG UK Properties: The Office Group, London flexible offices.", [5]),
 ("Zagrebtower: Zagreb office lease.", [7]),
 ("Innovent Spaces: Chennai coworking.", [8]),
 ("GPT Space & Co: Australian flexible workspace.", [11]),
 ("Work Easy Space Solutions: Indian coworking.", [63]),
 ("Common Desk: US coworking.", [118]),
 ("BDO LLP, Grant Thornton, PwC, Crowe Horwath Revizija, Collards, McBurneys, N S Shastri, Pinnacle Partnership, Taxstudio, Porezno Savjetništvo Tuk, Eurofast: audit, tax and accounting across the UK, Croatia, India, Greece.", [4, 29, 108, 114, 70, 153, 164, 109, 64, 176, 52]),
 ("Granttree: UK R&D tax credit claims consultancy paid as a share of the claim.", [68]),
 ("4i Advisory Services and 4i Management Consulting: Indian management and finance consulting, confirm scope.", [17, 72]),
 ("RSM UK Corporate Finance, Houlihan Lokey: M&A advisers.", [13, 35]),
 ("SS&C Intralinks: virtual data room.", [31]),
 ("Vector Capital Management: private equity sponsor fees, non-recurring after the sale.", [36]),
 ("Westbrook Advisers: advisory, scope unknown.", [62]),
 ("Jensten Insurance Brokers: UK commercial insurance broker.", [10]),
 ("Aetna, Agram Life, Care Health, Bupa (two entities), Cigna SG, ICICI Lombard, ICICI Prudential: employee health and life insurance by country.", [12, 42, 45, 47, 71, 69, 95, 143]),
 ("Allianz Australia Workers' Compensation and icare NSW: statutory workers' compensation.", [94, 201]),
 ("Mercer: benefits consulting.", [98]),
 ("Harmonic Group, Cedar Recruitment: finance recruitment agencies.", [21, 51]),
 ("Technet IT Recruitment: IT recruitment.", [49]),
 ("Accutrainee: legal trainee placement.", [33]),
 ("Info Edge: Naukri job board.", [138]),
 ("LinkedIn Ireland: recruiter licences, ads or Sales Navigator; default G&A recruiting, confidence medium.", [26]),
 ("HR Solution International GmbH and AG: HR outsourcing or employer of record in DACH.", [16, 90]),
 ("Australian Payroll Professionals: payroll outsourcing.", [111]),
 ("Radius Group: likely global payroll and expansion services, confidence low.", [179]),
 ("Peakon: employee engagement surveys.", [55]),
 ("Performancepro: performance management software.", [80]),
 ("Emerge Development Consultancy: leadership training.", [79]),
 ("Epignosis: TalentLMS.", [221]),
 ("Kryterion: certification exam delivery, likely for customer or partner certification.", [124]),
 ("Pluxee and Sodexo India: meal benefits and office catering.", [128, 54]),
 ("Benefit Systems d.o.o.: MultiSport employee sports card.", [57]),
 ("Green Commute Initiative: UK cycle-to-work scheme.", [100]),
 ("Inside Edge Novated Leasing: Australian salary-packaged car leasing.", [195]),
 ("Visalogic: UK immigration services.", [76]),
 ("Intertrust Singapore, Acclime (two entities), Capitol Services: corporate secretarial and registered agent.", [88, 99, 105, 334]),
 ("Computershare-Caboodle, Bigshare, NSDL: share plan administration and depository.", [211, 305, 284]),
 ("Raiffeisenbank Austria d.d.: Croatian bank fees.", [216]),
 ("FastSpring: merchant-of-record payment processing.", [198]),
 ("Ariba: SAP Ariba supplier network fees, customer-mandated.", [191]),
 ("Telefónica Global Services GmbH and Telefónica Compras Electrónicas: payments to a customer's procurement or partner platform, confidence low, flag as a commercial dependency, do not terminate.", [15, 93]),
 ("TM Forum (two spellings): telecom industry association membership and events.", [25, 249]),
 ("Terrapinn: conference organiser.", [150]),
 ("Big Frontier (Cult of Monday): Australian marketing agency.", [20]),
 ("MightyHive: programmatic media agency.", [50]),
 ("Plus Your Business: LinkedIn marketing training.", [56]),
 ("Uberflip: content experience platform.", [41]),
 ("Cognism, Lusha, 6sense: B2B contact and intent data.", [40, 156, 352]),
 ("Outreach: sales engagement.", [84]),
 ("Carrington Communications, Cision PR Newswire: PR.", [184, 168]),
 ("Smashing Media: UX publication and conferences.", [220]),
 ("Pixsy: image copyright monitoring.", [237]),
 ("Cloud Technology Solutions: UK Google Cloud and Workspace reseller.", [23]),
 ("New Star Networks: UK telecom and IT managed services.", [46]),
 ("Infosys, Shree Info System Solutions, Crayond Digital, Orionw, Trending Technology Services: outsourced IT and development, confirm whether customer-project subcontracting.", [19, 48, 185, 116, 213]),
 ("Magazin Računalni Sistemi, E-Disti, Sniper Systems: IT hardware resellers.", [66, 260, 131]),
 ("NCC Services: software escrow.", [144]),
 ("Bureau Veritas Croatia: ISO certification audits.", [142]),
 ("Centar za Sigurnost: occupational safety and fire protection services.", [106]),
 ("Nastavni Zavod za Javno Zdravstvo, Specijalistička ordinacija medicine rada (three), Ustanova za zdravstvenu skrb: statutory occupational health examinations.", [300, 382, 383, 384, 328]),
 ("Grad Zagreb, Grad Split: municipal fees.", [73, 139]),
 ("Zagrebački Holding: Zagreb city utilities.", [321]),
 ("HEP Elektra: electricity.", [119]),
 ("Hrvatski Telekom, Telemach, T-Mobile, Vodafone Australia, Starhub, BT, Inet Telecoms, Zettanet: telecom and internet.", [53, 104, 140, 135, 163, 188, 356, 306]),
 ("Avoxi: cloud telephony numbers.", [309]),
 ("Click Send: SMS API.", [363]),
 ("Studentski Centar (Zagreb, Split, Karlovac): Croatian student-service work contracts, contingent labour, not a vendor service.", [30, 86, 186]),
 ("Hrvatski Nezavisni Izvoznici Softvera, Split Tech City: industry and community memberships.", [318, 283]),
 ("Entrio: event ticketing.", [257]),
 ("Lajnap, Escape Art, Maniax, Sportkart, Paint & Fun, Paint&Wine, DJs For U, Blitz Cinestar, Good Game Global, Chamiers and P S Recreation Clubs, Sportska Udruga Split, Friends Sports Club: team events and recreation.", [187, 326, 277, 323, 183, 315, 298, 265, 146, 192, 197, 354, 227]),
 ("Konzum, Spar, Müller, Pepco, Ikea Hrvatska, Officeworks, Platinum Office, Roto Dinamic, Fero-Term, Brodomerkur: office groceries, supplies and furniture.", [61, 274, 207, 343, 136, 362, 358, 248, 327, 379]),
 ("Weking d.o.o., Veniture d.o.o., Nefron obrt, Bijeli Pijesak obrt, Smart Group Services, TP Prime, Pingo, Ramiro, Omonia, Mosaic Concept, Limes Plus, Orcola, Akton: Croatian companies or sole traders of unknown function, most likely contractors; department by best inference, confidence low, description ends with \"confirm with Finance\".", [9, 32, 38, 74, 58, 67, 65, 75, 83, 96, 97, 137, 141]),
 ("Stipe Piric, John Smith, Fabiola Thistlewhaite, George Anchor, Susan Lee, Ansar Madovic: individual payees, likely contractors or reimbursements, G&A, confidence low.", [160, 165, 166, 169, 177, 178]),
 ("(Blank): unnamed payee, G&A, Terminate, control gap.", [325]),
]
missing = [h for h, _ in H if h not in para]
print("hints not verbatim in log:", missing)
rebuilt = " ".join(h for h, _ in H)
print("hints rebuild the paragraph exactly:", rebuilt == para.strip())
rows = [r for _, rs in H for r in rs]
print("hinted rows:", len(rows), "unique:", len(set(rows)), "dupes:", sorted({r for r in rows if rows.count(r) > 1}))
for h, rs in H:
    print(h.split(":")[0][:60].ljust(60), "|", "; ".join(f"{r}={recs[r]['name_fixed']}" for r in rs))
json.dump([[h, rs] for h, rs in H], open(sys.argv[1], "w"), ensure_ascii=False)
