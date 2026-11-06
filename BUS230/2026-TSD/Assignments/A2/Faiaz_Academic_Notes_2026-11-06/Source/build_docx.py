from pathlib import Path
import json

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor


source = Path(__file__).resolve().parent
group_notes = source.parents[1] / 'Academic_Notes_2026-11-05/Source/Notes_Content_EN.json'
slides = [
    (13, 'The dependency register',
     'The dependency register links each working condition at Cedar Retail to the action that relies on it. The IT lead verifies scanner access by checking that the colleague can log in on the actual shift. The store manager checks that practice time is rostered and that the colleague has completed a realistic task. The sponsor records a decision and reason on the disputed penalty rule so the colleague knows which requirement applies. Burke and Litwin (1992) describe links among organisational factors and performance, while Herold, Fedor, and Caldwell (2007) examine how personal and contextual factors shape commitment to change. The register applies these perspectives by assigning responsibility for each condition and recording evidence that can be checked in context (Pettigrew, Woodman, and Cameron 2001).'),
    (14, 'One complete decision record',
     'The decision record brings the evidence for one task and colleague into a single place. The manager specifies the role, shift and task, records the relevant ADKAR need and proposed support, and identifies any missing condition or disputed requirement and its owner. Weiner (2009) explains that judgments about collective capability take account of task demands, available resources and the situation. Pettigrew, Woodman, and Cameron (2001) likewise emphasise the importance of studying change in context and over time. In the Cedar Retail example, the manager records a colleague’s explanation of the process as evidence about Knowledge and leaves Ability unverified until the task can be observed. The final fields capture the decision to continue, revise or pause, its reason and the condition that will trigger a review.'),
    (15, 'Implementation and owners',
     'Implementation begins with the store manager and colleague agreeing on the task, its scope and what would count as acceptable performance. IT resolves access issues, the manager arranges time for practice, and the sponsor addresses the disputed requirement. The colleague then practises with a coach under usable conditions so the manager can review performance against the criteria. The store manager records the decision and specifies when to reconsider it. Pettigrew, Woodman, and Cameron (2001) emphasise the relationship between the context and process of organisational change over time. In this workflow, the timing of practice and review depends on the conditions of the shift. Giving each prerequisite an owner makes it clear who can act when the colleague is ready to practise but the work environment is still preventing a fair demonstration.'),
    (16, 'Decisions on implementation',
     'The team proposes three decisions based on what the manager can verify. Continue when essential prerequisites are in place and observed task performance supports proceeding, with support and review as needed. Revise when a design choice or requirement needs reconsideration, such as the rule on penalties for inherited errors. Pause the affected task when an essential prerequisite is missing and assign its resolution to the relevant owner. Prosci’s ADKAR assessment guidance describes reassessment as a basis for adapting support (Prosci n.d.-d). Nilsen (2015) distinguishes guidance for implementation from evaluation of implementation. Our three decisions provide guidance for this case. Recording the reason and review trigger makes each judgment traceable and gives the manager a clear basis for reconsidering it when the evidence changes.'),
    (17, 'Feasibility and evaluation',
     'Cedar Retail could use one shared digital PDF record, with evidence beside each action and responsibility assigned to the existing store manager, IT lead and sponsor. Its practicality depends on whether those roles can resolve the conditions assigned to them and keep the record current within their existing workload. Nilsen (2015) distinguishes a process that guides implementation from the evaluation of what that process achieves. Errida and Lotfi (2021) identify change success factors in the literature and consider them in a construction company, which helps explain why suitability should be examined in the setting where a tool will be used. A Cedar Retail pilot would therefore review task accuracy, unresolved dependencies, the reasons given in response to concerns, and the time spent maintaining the record.'),
    (18, 'Risks and practical safeguards',
     'The safeguards address four ways the decision record could become less useful. The manager limits paperwork by recording essential fields for the affected task. A review date and escalation route give the manager a way to follow up when the sponsor has yet to respond. Agreeing on a representative task before assessing Ability gives the coach and colleague a shared standard for the demonstration. The record keeps gaps in the evidence visible, such as a scanner login that still fails on the relevant shift. Nilsen (2015) distinguishes guidance for action from evaluation, which explains why completed fields should be checked against actual task evidence. A pilot would test whether these safeguards help managers identify unresolved issues and make decisions before the record is used more widely.'),
]

references = json.loads(group_notes.read_text())['references']
prefixes = ('Burke,', 'Errida,', 'Herold,', 'Nilsen,', 'Pettigrew,', 'Prosci. n.d.-d.', 'Weiner,')
selected = [next(ref['text'] for ref in references if ref['text'].startswith(prefix)) for prefix in prefixes]

doc = Document()
page = doc.sections[0]
page.page_width, page.page_height = Inches(8.2677), Inches(11.6929)
page.top_margin, page.bottom_margin = Inches(.83), Inches(.75)
page.left_margin = page.right_margin = Inches(.86)
page.footer_distance = Inches(.35)
for name, size in [('Normal', 11.5), ('Title', 21), ('Heading 1', 13), ('Footer', 9)]:
    style = doc.styles[name]
    style.font.name, style.font.size = 'Arial', Pt(size)
    style.font.color.rgb = RGBColor(0, 0, 0)
    fonts = style.element.rPr.rFonts
    for attribute in ('asciiTheme', 'hAnsiTheme', 'eastAsiaTheme', 'cstheme'):
        fonts.attrib.pop(qn(f'w:{attribute}'), None)
    fonts.set(qn('w:eastAsia'), 'Arial')
doc.styles['Title'].font.bold = True
doc.styles['Title'].paragraph_format.space_after = Pt(8)
normal = doc.styles['Normal'].paragraph_format
normal.line_spacing = 1.24
normal.space_after = Pt(8)
normal.widow_control = True
heading = doc.styles['Heading 1'].paragraph_format
heading.space_before, heading.space_after = Pt(12), Pt(5)
heading.keep_with_next = True
heading.line_spacing = 1.1

footer = page.footer.paragraphs[0]
footer.alignment = WD_ALIGN_PARAGRAPH.RIGHT
field = OxmlElement('w:fldSimple')
field.set(qn('w:instr'), 'PAGE')
footer._p.append(field)

doc.add_paragraph('BUS230 Assessment 2 Academic Notes', style='Title')
p = doc.add_paragraph('Faiaz Dzhafarov  |  Class 2 Group 4')
p.runs[0].bold = True
doc.add_paragraph('Slides 13–18 explain how the proposed Cedar Retail decision record connects ADKAR support with working conditions, evidence and management decisions.')
for number, title, body in slides:
    p = doc.add_paragraph(f'Slide {number}  {title}', style='Heading 1')
    p.paragraph_format.page_break_before = number == 16
    doc.add_paragraph(body).paragraph_format.keep_together = True

p = doc.add_paragraph('References', style='Heading 1')
p.paragraph_format.page_break_before = True
for entry in selected:
    p = doc.add_paragraph()
    fmt = p.paragraph_format
    fmt.left_indent, fmt.first_line_indent = Inches(.25), Inches(-.25)
    fmt.space_after, fmt.line_spacing = Pt(10), 1.13
    fmt.keep_together = True
    for index, segment in enumerate(entry.split('*')):
        p.add_run(segment).italic = bool(index % 2)

for xml in (doc.styles.element, doc.element):
    for border in list(xml.iter(qn('w:pBdr'))):
        border.getparent().remove(border)

doc.core_properties.title = 'BUS230 Assessment 2 Academic Notes for Slides 13–18'
doc.core_properties.author = 'Faiaz Dzhafarov'
doc.core_properties.subject = 'Academic explanations for the Cedar Retail ADKAR presentation'
doc.core_properties.comments = ''
output = source.parent / 'BUS230_A2_Faiaz_Academic_Notes_Slides_13-18.docx'
doc.save(output)
print(output)
