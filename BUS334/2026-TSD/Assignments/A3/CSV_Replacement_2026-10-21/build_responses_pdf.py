from pathlib import Path
import csv, json, hashlib, re, unicodedata
from xml.sax.saxutils import escape
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Spacer, PageBreak
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from pypdf import PdfReader

BASE=Path(__file__).resolve().parent
RAW=BASE.parent/'Responses_2026-10-18/Google_Forms_Responses_2026-10-18.csv'
PDF=BASE/'35553299_Dzhafarov_BUS334_A3_Original_Responses.pdf'
records=list(csv.reader(RAW.open(encoding='utf-8-sig')))
headers,rows=records[0],records[1:]
assert len(rows)==22 and len(headers)==21 and all(len(r)==21 for r in rows)
pdfmetrics.registerFont(TTFont('SurveyArial','/System/Library/Fonts/Supplemental/Arial.ttf'))
pdfmetrics.registerFont(TTFont('SurveyArialBold','/System/Library/Fonts/Supplemental/Arial Bold.ttf'))
title=ParagraphStyle('Title',fontName='SurveyArialBold',fontSize=15,leading=18,spaceAfter=8)
meta=ParagraphStyle('Meta',fontName='SurveyArial',fontSize=9,leading=12,spaceAfter=5)
question=ParagraphStyle('Question',fontName='SurveyArial',fontSize=9.2,leading=11.4)
answer=ParagraphStyle('Answer',fontName='SurveyArial',fontSize=9.4,leading=11.6)
head=ParagraphStyle('Head',fontName='SurveyArialBold',fontSize=9.4,leading=12)
story=[]
for i,r in enumerate(rows,1):
    if i>1:story.append(PageBreak())
    story.append(Paragraph('Campus grocery survey responses',title))
    story.append(Paragraph(f'BUS334 Assignment 3 | Faiaz Dzhafarov | 35553299 | Respondent R{i:02} of 22',meta))
    story.append(Paragraph('Original submission timestamp: '+escape(r[0]),meta))
    story.append(Paragraph('Source: Google Forms CSV export, 18 October 2026. Questions and answers are reproduced verbatim. Semicolons in an answer retain multiple selections.',meta))
    story.append(Spacer(1,5))
    data=[[Paragraph('Question',head),Paragraph('Original answer',head)]]
    for h,v in zip(headers[1:],r[1:]):
        data.append([Paragraph(escape(h),question),Paragraph(escape(v),answer)])
    table=Table(data,colWidths=[286,225],repeatRows=1,hAlign='LEFT')
    table.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,0),colors.HexColor('#E1E8ED')),
        ('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,colors.HexColor('#F6F7F8')]),
        ('GRID',(0,0),(-1,-1),.4,colors.HexColor('#D9D9D9')),
        ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
        ('LEFTPADDING',(0,0),(-1,-1),6),('RIGHTPADDING',(0,0),(-1,-1),6),
        ('TOPPADDING',(0,0),(-1,-1),4),('BOTTOMPADDING',(0,0),(-1,-1),4)
    ]))
    story.append(table)

def footer(canvas,doc):
    canvas.saveState();canvas.setFont('SurveyArial',8)
    canvas.drawString(42,24,'BUS334 A3 | Original response evidence | 22 complete records')
    canvas.drawRightString(A4[0]-42,24,f'Page {doc.page} of 22');canvas.restoreState()

doc=SimpleDocTemplate(str(PDF),pagesize=A4,rightMargin=42,leftMargin=42,topMargin=34,bottomMargin=39,
                      title='Campus grocery survey original responses',author='Faiaz Dzhafarov')
doc.build(story,onFirstPage=footer,onLaterPages=footer)
reader=PdfReader(PDF)
assert len(reader.pages)==22, len(reader.pages)
def norm(s):return re.sub(r'\s+',' ',unicodedata.normalize('NFKC',s)).strip()
for i,(r,p) in enumerate(zip(rows,reader.pages),1):
    txt=norm(p.extract_text())
    assert f'Respondent R{i:02} of 22' in txt
    for value in headers[1:]+r:
        assert norm(value) in txt,(i,value)
qa={'source_csv':str(RAW.relative_to(BASE.parent)),'source_csv_sha256':hashlib.sha256(RAW.read_bytes()).hexdigest(),
    'pdf':PDF.name,'pdf_sha256':hashlib.sha256(PDF.read_bytes()).hexdigest(),
    'response_count':22,'question_count':20,'page_count':22,'one_respondent_per_page':True,
    'all_440_answers_match_source_verbatim':True,'all_22_timestamps_match_source':True,
    'all_20_question_headers_present_for_each_respondent':True,
    'purpose':'Replace unsupported CSV in the third Moodle submission slot with readable PDF evidence; original CSV and prior submission evidence are preserved.',
    'visual_review':'pending','lms_replacement_status':'not yet performed'}
(BASE/'VERIFICATION.json').write_text(json.dumps(qa,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(qa,ensure_ascii=False,indent=2))
