#!/usr/bin/env python3
# Build final BUS293 Team Report (Group 11) .docx from the Google Doc source text.
import re, os, sys
try:
    from docx import Document
    from docx.shared import Pt, RGBColor, Inches
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.enum.table import WD_TABLE_ALIGNMENT
    from docx.oxml.ns import qn
    from docx.oxml import OxmlElement
except ImportError:
    os.system(f"{sys.executable} -m pip install --quiet python-docx")
    from docx import Document
    from docx.shared import Pt, RGBColor, Inches
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.enum.table import WD_TABLE_ALIGNMENT
    from docx.oxml.ns import qn
    from docx.oxml import OxmlElement

SRC = "/Users/king1/Downloads/BUS293_whatsapp/_txt/GoogleDoc_FINAL.txt"
OUTDIR = "/Users/king1/Documents/Murdoch/BUS293"
os.makedirs(OUTDIR, exist_ok=True)
OUT = os.path.join(OUTDIR, "BUS293_Team_Report_Group11_FINAL.docx")

lines = open(SRC, encoding="utf-8").read().split("\n")

def idx(marker, after=0):
    for i in range(after, len(lines)):
        if lines[i].strip().startswith(marker):
            return i
    return -1

body0 = idx("3.   Identified Challenges", after=60)
intro_i = idx("2.   Introduction", 60)
I = {
 "es":   idx("1.   Executive Summary", 60),
 "intro":intro_i,
 "2a": idx("2.a", intro_i+1), "2b": idx("2.b", intro_i+1),
 "2c": idx("2.c", intro_i+1), "2d": idx("2.d", intro_i+1),
 "ch":   body0,
 "3a": idx("3.a", body0), "3b": idx("3.b", body0),
 "3c": idx("3.c", body0), "3d": idx("3.d", body0),
 "rec":  idx("4.   Recommendations", body0),
 "con":  idx("5.  Conclusion", body0),
 "ref":  idx("6.   Reference List", body0),
 "app":  idx("7. Appendices", body0),
}

def _wc(s, e):
    return sum(len(re.findall(r"\b[\w'-]+\b", l)) for l in lines[s+1:e])
DISC_WC = (_wc(I["3a"], I["3b"]) + _wc(I["3b"], I["3c"])
           + _wc(I["3c"], I["3d"]) + _wc(I["3d"], I["rec"]))

def paras(s, e):
    out = []
    for l in lines[s+1:e]:
        t = l.strip()
        if t:
            out.append(re.sub(r"\s{2,}", " ", t))
    return out

doc = Document()
st = doc.styles["Normal"]
st.font.name = "Times New Roman"
st.font.size = Pt(12)
st.element.rPr.rFonts.set(qn("w:eastAsia"), "Times New Roman")
for sec in doc.sections:
    sec.top_margin = Inches(1); sec.bottom_margin = Inches(1)
    sec.left_margin = Inches(1); sec.right_margin = Inches(1)

def body_par(text, justify=True, italic=False, size=12):
    p = doc.add_paragraph()
    r = p.add_run(text); r.italic = italic; r.font.size = Pt(size)
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY if justify else WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_after = Pt(8)
    p.paragraph_format.line_spacing = 1.15
    return p

def h(text, level=1):
    text = re.sub(r"\s*\((Bobur|Faiaz|Owethu|Faiaz Dzhafarov)\)\s*$", "", text)
    text = re.sub(r"\s{2,}", " ", text.strip())
    p = doc.add_heading(level=level)
    r = p.add_run(text)
    r.font.name = "Times New Roman"
    r.font.color.rgb = RGBColor(0, 0, 0)
    r.font.size = Pt(16 if level == 1 else 13)
    return p

def subhead(text):
    p = doc.add_paragraph()
    r = p.add_run(text); r.bold = True; r.font.size = Pt(12)
    p.paragraph_format.space_before = Pt(6); p.paragraph_format.space_after = Pt(4)
    return p

def render_block(s, e):
    for t in paras(s, e):
        if re.match(r"(?i)^potential recommendations?:?$", t):
            subhead("Potential solutions")
        elif re.match(r"^\d+\.\s", t):
            p = doc.add_paragraph(t)
            p.paragraph_format.left_indent = Inches(0.3)
            p.paragraph_format.space_after = Pt(2)
        else:
            body_par(t)

def cover():
    for _ in range(2): doc.add_paragraph()
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run("Team Dynamics at\nWestpac Banking Corporation")
    r.bold = True; r.font.size = Pt(28)
    p2 = doc.add_paragraph(); p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r2 = p2.add_run("Organisational Behaviour Challenges and Recommendations")
    r2.italic = True; r2.font.size = Pt(14)
    for _ in range(2): doc.add_paragraph()

    def field(label, value, bold_val=False):
        pp = doc.add_paragraph(); pp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        a = pp.add_run(label + "  "); a.bold = True; a.font.size = Pt(12)
        b = pp.add_run(value); b.bold = bold_val; b.font.size = Pt(12)
        pp.paragraph_format.space_after = Pt(2)

    field("Unit Code & Title:", "BUS293 Organisational Theory and Behaviour (TMD 2026)")
    field("Report Topic:", "Team Dynamics")
    field("Group:", "11")
    doc.add_paragraph()
    t = doc.add_table(rows=1, cols=2); t.alignment = WD_TABLE_ALIGNMENT.CENTER
    t.style = "Table Grid"
    for c, txt in zip(t.rows[0].cells, ["Student Name", "Student Number"]):
        rr = c.paragraphs[0].add_run(txt); rr.bold = True
        c.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
    for name, num in [("Bobur Yorikhanov", "35676172"),
                      ("Faiaz Dzhafarov", "35553299"),
                      ("Owethu Thabethe", "34321625")]:
        cells = t.add_row().cells
        cells[0].text = name; cells[1].text = num
        for cc in cells: cc.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
    doc.add_paragraph()
    field("Workshop Day & Time:", "Wednesday, [time — confirm with group]")
    field("Workshop Facilitator:", "Harshini Esther")
    field("Unit Coordinator:", "Dr Farheen Javed")
    field("Word Count (discussion):", f"{DISC_WC:,} words")
    doc.add_page_break()

def toc():
    h("Contents", level=1)
    p = doc.add_paragraph()
    run = p.add_run()
    fb = OxmlElement('w:fldChar'); fb.set(qn('w:fldCharType'), 'begin')
    ins = OxmlElement('w:instrText'); ins.set(qn('xml:space'), 'preserve')
    ins.text = r'TOC \o "1-2" \h \z \u'
    fs = OxmlElement('w:fldChar'); fs.set(qn('w:fldCharType'), 'separate')
    tt = OxmlElement('w:t'); tt.text = "Right-click → Update Field to build the table of contents."
    fe = OxmlElement('w:fldChar'); fe.set(qn('w:fldCharType'), 'end')
    for el in (fb, ins, fs, tt, fe):
        run._r.append(el)
    doc.add_page_break()

RECS = [
 ("Integrate workshops on psychological safety and open communication, and appoint an in-house psychologist.",
  "Creates an environment where positive conversations are encouraged and employees do not feel undervalued. An in-house psychologist gives staff a resource for work or personal difficulties, removes the stigma around psychological-safety topics and makes employees more inclined to reach out."),
 ("Introduce annual team-building exercises and retreats.",
  "With a hybrid policy and multiple Australian locations, yearly retreats help employees across all levels network, build relationships and grow team trust in a setting free of day-to-day work pressure."),
 ("Establish confidential channels for employees to voice concerns.",
  "Confidentiality is paramount for sensitive situations. When employees know confidentiality is valued, they feel safe to speak up without fear of judgement, reinforcing psychological safety and anti-corruption (Principle 10)."),
 ("Implement organisation-wide collaboration mechanisms and encourage cross-team engagement.",
  "Ensures constant collaboration and communication across departments, so employees are comfortable working together, producing a more cohesive work environment throughout the organisation."),
 ("Introduce ongoing review measures of employee satisfaction, departmental-system efficiency and feedback-tool integration.",
  "Demonstrates WBC's commitment to consistency across the organisation and the employee experience, and allows problems to be detected and corrected early."),
]
def recommendations():
    h("4. Recommendations", level=1)
    body_par("Drawing on the analysis above, the team identified the five most relevant "
             "recommendations for Westpac Banking Corporation. Each is paired with its benefit "
             "to link the action explicitly to organisational needs.")
    t = doc.add_table(rows=1, cols=2); t.style = "Table Grid"
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    for c, txt in zip(t.rows[0].cells, ["Recommendation", "Benefit(s) of implementation"]):
        rr = c.paragraphs[0].add_run(txt); rr.bold = True
    for i, (rec, ben) in enumerate(RECS, 1):
        cells = t.add_row().cells
        cells[0].text = f"{i}. {rec}"
        cells[1].text = ben
    for row in t.rows:
        row.cells[0].width = Inches(2.4); row.cells[1].width = Inches(4.1)

def references():
    h("6. Reference List", level=1)
    for t in paras(I["ref"], I["app"]):
        p = doc.add_paragraph()
        p.add_run(t).font.size = Pt(12)
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.left_indent = Inches(0.5)
        p.paragraph_format.first_line_indent = Inches(-0.5)
        p.paragraph_format.space_after = Pt(6)

def appendices():
    h("7. Appendices", level=1)

    h("Appendix A — Summary of the Four Team-Dynamics Challenges", level=2)
    colsA = ["Challenge", "Key OB theory / concept", "Effect on performance",
             "Effect on sustainability", "UN Global Compact principle", "Illustrative source"]
    rowsA = [
      ["Communication problems between teams",
       "Team mental models (Kozlowski & Ilgen 2006)",
       "Slower decisions, weaker service quality, higher operational risk",
       "Employee stress, compliance and regulatory exposure",
       "Principle 10 — transparency & anti-corruption",
       "Mathieu et al. 2008"],
      ["Team trust",
       "Three foundations: integrity, benevolence, ability (Mayer et al. 1995); swift trust (Meyerson et al. 1996)",
       "Faster information flow and coordination",
       "Retention, willingness to report risk",
       "Principle 10 — anti-corruption",
       "AUSTRAC 2020"],
      ["Remote / hybrid work",
       "Virtual teams; work–family conflict (Junça Silva & Lopes 2025)",
       "Reduced cohesion and morale; legal disputes",
       "Employee well-being and retention",
       "Principle 4 — elimination of forced & compulsory labour (as argued in §3.c)",
       "Karlene Chandler v Westpac 2025 (FWC 3115)"],
      ["Collaboration & cohesion across departments",
       "Group cohesion (Beal et al. 2003); cross-functional teams",
       "Coordination across functional silos",
       "Engagement and knowledge sharing",
       "Principle 10 — accountability",
       "Salas, Sims & Burke 2005"],
    ]
    tA = doc.add_table(rows=1, cols=len(colsA)); tA.style = "Table Grid"
    for c, txt in zip(tA.rows[0].cells, colsA):
        r = c.paragraphs[0].add_run(txt); r.bold = True; r.font.size = Pt(9)
    for row in rowsA:
        cells = tA.add_row().cells
        for c, txt in zip(cells, row):
            c.paragraphs[0].add_run(txt).font.size = Pt(9)
    body_par("Source: authors' synthesis of the report's analysis and cited literature.",
             italic=True, size=9)
    doc.add_paragraph()

    h("Appendix B — The Three Foundations of Trust (Mayer, Davis & Schoorman 1995)", level=2)
    colsB = ["Foundation", "What it means", "What erodes it at WBC"]
    rowsB = [
      ["Integrity", "The person is seen as honest and principled, holding to values the other party accepts.",
       "Inconsistent messaging or perceived unfairness between departments."],
      ["Benevolence", "The person is seen as genuinely caring about the other's wellbeing, beyond self-interest.",
       "A sense that managers prioritise targets over the people meeting them."],
      ["Ability", "The person is seen as competent and skilled in the relevant domain.",
       "Doubt that another department can supply accurate, timely information."],
    ]
    tB = doc.add_table(rows=1, cols=3); tB.style = "Table Grid"
    for c, txt in zip(tB.rows[0].cells, colsB):
        r = c.paragraphs[0].add_run(txt); r.bold = True; r.font.size = Pt(10)
    for row in rowsB:
        cells = tB.add_row().cells
        for c, txt in zip(cells, row):
            c.paragraphs[0].add_run(txt).font.size = Pt(10)
    body_par("Trust builds slowly but collapses quickly: a weakness in any one foundation, or a single "
             "communication failure, can undermine it (Greenberg & Baron 2008). In dispersed teams, "
             "clear roles and dependable processes support “swift trust” before personal "
             "familiarity has formed (Meyerson, Weick & Kramer 1996).", italic=True, size=10)
    doc.add_paragraph()

    h("Appendix C — Westpac AUSTRAC 2020 Case Snapshot", level=2)
    rowsC = [
      ["Date", "September 2020"],
      ["Breach", "More than 23 million breaches of the Anti-Money-Laundering and Counter-Terrorism-Financing Act"],
      ["Penalty", "A$1.3 billion — a record civil penalty in Australian corporate history"],
      ["Root causes", "Failures of transaction monitoring and internal escalation of risk"],
      ["Relevance to this report",
       "Illustrates how weak trust and low psychological safety let operational risks go unreported; "
       "directly informs WBC's later focus on conduct and risk culture and its alignment with UN Global Compact Principle 10."],
      ["Sources", "AUSTRAC 2020; Westpac Banking Corporation 2024"],
    ]
    tC = doc.add_table(rows=1, cols=2); tC.style = "Table Grid"
    for c, txt in zip(tC.rows[0].cells, ["Item", "Detail"]):
        r = c.paragraphs[0].add_run(txt); r.bold = True; r.font.size = Pt(10)
    for row in rowsC:
        cells = tC.add_row().cells
        cells[0].paragraphs[0].add_run(row[0]).bold = True
        cells[1].paragraphs[0].add_run(row[1]).font.size = Pt(10)
        cells[0].width = Inches(1.6); cells[1].width = Inches(4.9)

cover()
toc()
h("1. Executive Summary", level=1); render_block(I["es"], I["intro"])
h("2. Introduction", level=1)
h(lines[I["2a"]], level=2); render_block(I["2a"], I["2b"])
h(lines[I["2b"]], level=2); render_block(I["2b"], I["2c"])
h(lines[I["2c"]], level=2); render_block(I["2c"], I["2d"])
h(lines[I["2d"]], level=2); render_block(I["2d"], I["ch"])
h("3. Identified Challenges", level=1)
h(lines[I["3a"]], level=2); render_block(I["3a"], I["3b"])
h(lines[I["3b"]], level=2); render_block(I["3b"], I["3c"])
h(lines[I["3c"]], level=2); render_block(I["3c"], I["3d"])
h(lines[I["3d"]], level=2); render_block(I["3d"], I["rec"])
recommendations()
h("5. Conclusion", level=1); render_block(I["con"], I["ref"])
references()
appendices()
doc.save(OUT)
print("SAVED:", OUT)
print("Paragraphs:", len(doc.paragraphs), "Tables:", len(doc.tables))
print("Index map:", I)
