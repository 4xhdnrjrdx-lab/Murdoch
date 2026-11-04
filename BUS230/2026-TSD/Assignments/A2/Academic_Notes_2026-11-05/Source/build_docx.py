import json, pathlib, re
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.enum.text import WD_ALIGN_PARAGRAPH

HERE=pathlib.Path(__file__).resolve().parent
data=json.loads((HERE/'Notes_Content_EN.json').read_text())
output=HERE/'BUS230Assessment2Class2Group4_AcademicNotes_2026-11-05.docx'
doc=Document()
section=doc.sections[0]
section.page_width=Inches(8.2677);section.page_height=Inches(11.6929)
section.top_margin=section.bottom_margin=Inches(.8)
section.left_margin=section.right_margin=Inches(.9)
section.header_distance=section.footer_distance=Inches(.35)
for name in ['Normal','Title','Subtitle','Heading 1','Heading 2','Header','Footer']:
    s=doc.styles[name]
    s.font.name='Arial';s.font.color.rgb=RGBColor(0,0,0)
    s.element.rPr.rFonts.set(qn('w:eastAsia'),'Arial')
    s.font.size=Pt(12)
normal=doc.styles['Normal'].paragraph_format
normal.line_spacing=1.5;normal.space_after=Pt(7)
normal.widow_control=True
title=doc.styles['Title'];title.font.size=Pt(22);title.font.bold=True
title.paragraph_format.space_after=Pt(10)
heading=doc.styles['Heading 1'];heading.font.size=Pt(13);heading.font.bold=True
heading.paragraph_format.space_before=Pt(15);heading.paragraph_format.space_after=Pt(6)
heading.paragraph_format.keep_with_next=True
heading.paragraph_format.line_spacing=1.1
doc.styles['Heading 2'].font.size=Pt(12)
doc.styles['Heading 2'].font.bold=True
doc.styles['Heading 2'].paragraph_format.keep_with_next=True

header=section.header.paragraphs[0]
header.text='BUS230 Assessment 2  |  Class 2 Group 4'
header.style='Header'
header.runs[0].font.size=Pt(9)
footer=section.footer.paragraphs[0];footer.alignment=WD_ALIGN_PARAGRAPH.RIGHT
footer.add_run('Page ').font.size=Pt(9)
field=OxmlElement('w:fldSimple');field.set(qn('w:instr'),'PAGE');footer._p.append(field)

doc.add_paragraph('BUS230 Assessment 2\nAcademic Supporting Notes',style='Title')
p=doc.add_paragraph('Using ADKAR with Context and Evidence')
p.paragraph_format.space_after=Pt(5)
p.runs[0].bold=True
p=doc.add_paragraph('Class 2 Group 4\nMohammad Mazin Mohammad Al Mili · Beryl Soria\nFaiaz Dzhafarov · Aram Avetisyan\n5 November 2026')
p.paragraph_format.line_spacing=1.15
p.paragraph_format.space_after=Pt(12)
doc.add_paragraph('These notes explain the content and academic reasoning of slides 1–30. The central proposal retains ADKAR and connects individual support with working conditions, responsibility and evidence. Cedar Retail is a fictional teaching case; the proposed decision record requires a pilot before its effectiveness can be established.')

for slide in data['slides']:
    # Preserve exact slide wording while using plain headings in the document.
    t=slide['title'].replace('01 / ','').replace('02 / ','').replace('03 / ','')
    t=t.replace(':','').replace(',','').replace('–',' to ')
    doc.add_paragraph(f"Slide {slide['slide']}  {t}",style='Heading 1')
    for i,paragraph in enumerate(slide['paragraphs']):
        p=doc.add_paragraph(paragraph)
        p.paragraph_format.keep_together=True
        p.paragraph_format.keep_with_next=i < len(slide['paragraphs'])-1

p=doc.add_paragraph('References',style='Heading 1')
p.paragraph_format.page_break_before=True
doc.add_paragraph('Academic sources',style='Heading 2')

def add_reference(ref):
    p=doc.add_paragraph()
    f=p.paragraph_format;f.left_indent=Inches(.25);f.first_line_indent=Inches(-.25)
    f.line_spacing=1.0;f.space_after=Pt(8);f.keep_together=True
    # Existing bibliography marks journal titles with asterisks.
    for i,part in enumerate(ref['text'].split('*')):
        r=p.add_run(part);r.italic=bool(i%2)
    return p

for ref in data['references']:
    if ref['kind']=='academic':add_reference(ref)
doc.add_paragraph('Professional and model sources',style='Heading 2')
for ref in data['references']:
    if ref['kind']=='professional':add_reference(ref)
doc.core_properties.title=data['title']
doc.core_properties.subject='Academic explanations for slides 1–30 of Using ADKAR with Context and Evidence'
doc.core_properties.author='Class 2 Group 4'
doc.core_properties.keywords='BUS230; Assessment 2; ADKAR; Academic notes'
doc.core_properties.comments=''
for tree in [doc.styles.element,doc.element]:
    for border in list(tree.iter(qn('w:pBdr'))):
        border.getparent().remove(border)
doc.save(output)
print(output)
