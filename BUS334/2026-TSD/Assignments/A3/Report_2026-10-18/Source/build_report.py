from pathlib import Path
import csv, json, re, hashlib, shutil, subprocess, os
from collections import Counter
from reportlab.graphics.shapes import Drawing, Rect, Line, String
from reportlab.graphics import renderPDF
from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from docx import Document
from docx.shared import Inches, Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

BASE = Path(__file__).resolve().parents[1]
COURSE = BASE.parents[2]
DATA = BASE.parent / 'Responses_2026-10-18'
RAW = DATA / 'Google_Forms_Responses_2026-10-18.csv'
SUMMARY = json.loads((DATA / 'SUMMARY.json').read_text())
QUESTIONS = SUMMARY['questions']
TABLE = list(csv.reader(RAW.open(encoding='utf-8-sig')))
HEADERS, ROWS = TABLE[0], TABLE[1:]
N = len(ROWS)
assert N == 22 and all(len(r) == 21 and all(v.strip() for v in r) for r in ROWS)
CHARTS = BASE / 'Charts'
CHARTS.mkdir(parents=True, exist_ok=True)
FONTCONFIG = Path('/private/tmp/bus334-fontconfig')
FONTCONFIG.mkdir(exist_ok=True)
(FONTCONFIG/'cache').mkdir(exist_ok=True)
(FONTCONFIG/'fonts.conf').write_text('<?xml version="1.0"?><!DOCTYPE fontconfig SYSTEM "fonts.dtd"><fontconfig><dir>/System/Library/Fonts</dir><dir>/Library/Fonts</dir><cachedir>/private/tmp/bus334-fontconfig/cache</cachedir></fontconfig>')
os.environ['FONTCONFIG_FILE'] = str(FONTCONFIG/'fonts.conf')
pdfmetrics.registerFont(TTFont('ChartArial','/System/Library/Fonts/Supplemental/Arial.ttf'))
pdfmetrics.registerFont(TTFont('ChartArialBold','/System/Library/Fonts/Supplemental/Arial Bold.ttf'))
BLUE = '#355B78'
GRAY = '#A4B6C3'

def bars(d, x, y, width, height, labels, values, title, colors=None):
    left = 93 if width < 300 else 110
    plot = width-left-52
    d.add(String(x, y+height-14, title, fontName='ChartArialBold',fontSize=10))
    top=y+height-38
    bottom=y+27
    step=(top-bottom)/max(len(labels)-1,1)
    for tick in [0,5,10,15,22]:
        xx=x+left+plot*tick/22
        d.add(Line(xx,bottom-10,xx,top+10,strokeColor=HexColor('#E6E9EC'),strokeWidth=.4))
        d.add(String(xx,bottom-21,str(tick),textAnchor='middle',fontName='ChartArial',fontSize=7,fillColor=HexColor('#555555')))
    for i,(label,count) in enumerate(zip(labels,values)):
        yy=top-i*step
        d.add(String(x,yy-3,label,fontName='ChartArial',fontSize=8,fillColor=HexColor('#222222')))
        d.add(Rect(x+left,yy-5,plot*count/22,10,fillColor=HexColor(colors[i] if colors else BLUE),strokeWidth=0))
        d.add(String(x+width,yy-3,f'{count} ({count/N:.1%})',textAnchor='end',fontName='ChartArial',fontSize=7.7))
    d.add(String(x+left+plot/2,y-6,'Number of respondents',textAnchor='middle',fontName='ChartArial',fontSize=7.5))

def save_chart(d, stem):
    pdf=CHARTS/(stem+'.pdf')
    renderPDF.drawToFile(d,str(pdf))
    subprocess.run(['/Users/king1/.cache/codex-runtimes/codex-primary-runtime/dependencies/bin/override/pdftoppm',
                    '-singlefile','-r','300','-png',str(pdf),str(CHARTS/stem)],check=True,timeout=40,capture_output=True)

fig=Drawing(504,191)
bars(fig,0,17,242,172,['Very dissatisfied','Dissatisfied','Neutral','Satisfied','Very satisfied'],
     [0,4,11,7,0],'Current satisfaction  Q8',[GRAY,GRAY,BLUE,GRAY,GRAY])
bars(fig,262,17,242,172,['Very unlikely','Unlikely','Neutral','Likely','Very likely'],
     [0,0,6,11,5],'Intention to shop  Q9',[GRAY,GRAY,GRAY,BLUE,BLUE])
save_chart(fig,'01_satisfaction_and_intention')
fig=Drawing(504,295)
bars(fig,0,174,242,120,['Snacks and drinks','Meals and fruit','Take home groceries','Care and stationery'],
     [15,8,0,0],'Products  Q12')
bars(fig,262,174,242,120,['Below AED 10','AED 10 to 24.99','AED 25 to 49.99','AED 50 or more'],
     [6,13,3,0],'Expected spend  Q11')
bars(fig,0,18,504,141,['5 or more per week','2 to 4 per week','Once per week','1 to 3 per month','Less than monthly'],
     [0,8,7,7,0],'Expected visits during teaching weeks  Q10')
save_chart(fig,'02_products_spend_and_visits')
fig=Drawing(504,205)
bars(fig,0,18,242,185,['Price','Product choice','Freshness','Opening hours','Quick checkout'],
     [15,3,1,0,3],'Main choice factor  Q17')
bars(fig,262,18,242,185,['Higher prices','Limited choice','Long queues','Unsuitable hours','Current alternatives','Nothing'],
     [15,4,3,0,0,0],'Main barrier  Q19')
save_chart(fig,'03_factors_and_barriers')

PAGES = [
[
('title', 'Campus grocery store feasibility'),
('subtitle', 'BUS334 Assignment 3  Data collection and preliminary analysis'),
('meta', 'Faiaz Dzhafarov  |  Student ID 35553299  |  18 October 2026'),
('h1', 'Part 1  Summary'),
('p', 'A small grocery store on the Murdoch University Dubai campus may attract students if it offers affordable snacks, drinks and quick meals. In this survey, 16 of 22 respondents (72.7%) said they were likely or very likely to use it at prices similar to nearby shops. Price was the main choice factor for 15 respondents (68.2%), and the same number selected higher prices as the main barrier. These findings support testing a small store before committing to a larger investment. They do not establish profitability.'),
('p', 'I collected 22 complete Google Forms responses from students through a private Telegram group of Russian-speaking Murdoch peers and approximately 10 personal WhatsApp invitations. The overall response rate is unknown because I do not know the total number reached through the group or the overlap between the two channels.'),
('h1', 'Part 2  Results'),
('h2', 'Data collection and preparation'),
('p', 'The questionnaire contained 20 questions: 19 closed questions and one open question. The export records all submissions on 18 October 2026. All 22 respondents answered every question, exceeding the minimum of 15 complete questionnaires. The completion rate among returned questionnaires was 100%; this is different from the invitation response rate.'),
('p', 'Checks of the original CSV found no missing answers, invalid options or repeated answer sets. The anonymous form did not collect names or email addresses, so these checks cannot independently verify identities. All 22 records were retained. Appendix A contains the questionnaire and counts, Appendix B gives the coded records, and Appendix C contains the written answers. The original CSV accompanies the appendices.'),
],
[
('h1', 'Part 2  Results continued'),
('h2', 'Sample and current shopping habits'),
('p', 'All respondents identified as students: 15 undergraduates and seven postgraduates. Most attended campus three or four days a week (18 of 22, 81.8%), so the sample had regular contact with the campus. The profile is reasonably balanced by gender, but recruitment through one social network limits its coverage.'),
('profile', None),
('p', 'Nearby supermarkets or convenience stores were selected by nine respondents (40.9%) as a usual source of purchases, compared with five for the campus cafe (22.7%). Eight respondents (36.4%) had left campus to buy food or daily items during the previous month. Four were dissatisfied with existing options, 11 were neutral and seven were satisfied. This suggests some room for a convenient alternative, without evidence of widespread dissatisfaction.'),
('figure', ('01_satisfaction_and_intention.png', 2.50)),
('caption', 'Figure 1  Current satisfaction and intention to shop. Source: Google Forms survey, 18 October 2026, n = 22. Each panel is a separate question.'),
],
[
('h1', 'Part 2  Results continued'),
('h2', 'Expected demand and product range'),
('p', 'Intention to shop was positive for 16 respondents, while six were neutral and none selected unlikely. This answer assumed suitable products and prices similar to nearby shops. It describes interest under those conditions, rather than guaranteed purchases.'),
('figure', ('02_products_spend_and_visits.png', 3.85)),
('caption', 'Figure 2  Proposed purchases, spending and visits. Source: survey, n = 22. Q12 allowed multiple selections; its percentages total more than 100%.'),
('p', 'Snacks and drinks received 15 selections (68.2%), followed by meals and fruit with eight (36.4%). Nobody selected take home groceries or personal care and stationery. Thirteen respondents (59.1%) expected to spend AED 10 to 24.99 per visit. Fifteen (68.2%) expected at least weekly visits, but none expected five or more visits per week. A limited range of inexpensive items therefore looks more suitable for a first trial than a full supermarket.'),
('p', 'Positive intention was 12 of 15 among undergraduates (80.0%) and four of seven among postgraduates (57.1%). These small groups describe this sample only; the difference is not evidence of a campus-wide pattern.'),
],
[
('h1', 'Part 2  Results continued'),
('h2', 'Price and the store offer'),
('figure', ('03_factors_and_barriers.png', 2.65)),
('caption', 'Figure 3  Choice factors and barriers. Source: survey, n = 22. These were separate single-choice questions, so the two groups of 15 need not contain the same people.'),
('p', 'The price example also showed resistance to a premium: 21 respondents (95.5%) chose AED 5.00 as the most they would pay when a nearby shop charged that amount, and one chose less. No respondent chose a higher price. This is a hypothetical comparison, not a verified market price. Eleven respondents (50.0%) preferred an ID discount as an incentive, while seven (31.8%) preferred meal bundles.'),
('p', 'A mini-market with fresh and ready-to-eat food received 11 selections (50.0%), and a small convenience kiosk received 10 (45.5%). Convenience near classes was selected as a reason to shop by nine students (40.9%); emergency purchases received six selections (27.3%). These findings favour a compact store serving short campus breaks. Social media received eight selections (36.4%) as a preferred promotion channel, WhatsApp or student groups seven (31.8%), university email six and campus posters two.'),
('h2', 'Written responses'),
('p', 'The open answers repeatedly connected convenience with affordable prices. Thirteen of 22 explicitly mentioned price or affordability. R08 wrote, "Having a store nearby would save time, as long as it is not more expensive than outside." R09 usually brought food but saw value when something was forgotten. These comments help explain interest in small, occasional purchases. Appendix C lists every answer and the coding rule for the price theme.'),
],
[
('h1', 'Part 3  Preliminary conclusions next steps and recommendations'),
('p', 'The survey supports a small trial of a campus convenience store. Interest is strongest for snacks, drinks and quick meals at prices comparable to nearby shops. It provides a basis for choosing a trial range, but the decision to open permanently still requires costs and actual sales evidence.'),
('h2', 'Recommendations'),
('p', 'Start with a compact range of snacks and drinks, with a small selection of fresh meals or fruit. This follows the 15 and eight selections for those categories. Avoid committing much initial stock to take home groceries or stationery, which received no selections in this sample. A short trial could compare the kiosk and small mini-market formats.'),
('p', 'Check supplier prices and campus operating costs before setting retail prices. Test affordable meal bundles and an ID discount, since these attracted seven and 11 responses respectively. The water question gives no evidence that this sample would accept a campus price premium. Discounts should depend on margins rather than being promised in advance.'),
('p', 'During a trial, record actual transactions, basket values, repeat visits and unsold fresh stock. Compare these with staffing, rent and supply costs before estimating break-even sales. Promote the trial through social media and student groups, then measure which channel brings customers.'),
('h2', 'Limitations and further research'),
('p', 'This is a convenience sample of 22 students. The Telegram group and personal invitations may favour similar social networks and language backgrounds. Neither the sample size nor the balanced gender split makes it representative of the university. The number invited is unknown, so an overall response rate cannot be calculated.'),
('p', 'Five questions used checkboxes despite asking for a MOST or MAIN choice. Q6, Q12, Q15 and Q16 each recorded 23 selections from 22 people. I kept these selections and calculated each percentage using 22 respondents. Q18 also ends with an incomplete phrase, which may affect interpretation. Before another survey, I would complete that wording, use single-choice fields where one priority is required, and pilot the questions.'),
('p', 'A further survey should recruit across programmes, campus days and student networks, with a clear invitation count. It should test actual product prices and ask when students would visit. The present findings justify further testing; they do not measure demand across the whole campus or establish that the store would earn a profit.'),
('source', 'Data source: author survey, Google Forms export, 18 October 2026, 22 records. Questionnaire, individual response evidence and all open answers appear in the separate appendices and accompanying CSV.'),
]
]

def shade(cell, fill):
    pr = cell._tc.get_or_add_tcPr()
    e = OxmlElement('w:shd'); e.set(qn('w:fill'), fill); pr.append(e)

def document(appendix=False):
    d = Document()
    s = d.sections[0]
    s.page_height = Cm(29.7); s.page_width = Cm(21)
    s.top_margin = Cm(1.75); s.bottom_margin = Cm(1.7)
    s.left_margin = Cm(1.8); s.right_margin = Cm(1.8)
    s.header_distance = Cm(.7); s.footer_distance = Cm(.7)
    for name in ['Normal','Title','Subtitle','Heading 1','Heading 2','Caption']:
        st = d.styles[name]
        st.font.name = 'Arial'; st.font.color.rgb = RGBColor(0,0,0)
    normal = d.styles['Normal']; normal.font.size = Pt(10.5 if appendix else 11)
    normal.paragraph_format.line_spacing = 1.15 if appendix else 1.5
    normal.paragraph_format.space_after = Pt(6)
    for name,size in [('Title',20),('Subtitle',11),('Heading 1',14),('Heading 2',11.5),('Caption',9)]:
        st = d.styles[name]; st.font.size = Pt(size)
        st.paragraph_format.space_before = Pt(9 if name.startswith('Heading') else 0)
        st.paragraph_format.space_after = Pt(6)
        st.paragraph_format.line_spacing = 1.1
        if name.startswith('Heading'): st.font.bold = True
    d.styles['Title'].paragraph_format.space_after = Pt(8)
    d.styles['Caption'].font.italic = False
    d.styles['Caption'].font.bold = False
    d.styles['Caption'].paragraph_format.space_after = Pt(8)
    for st in d.styles:
        if st.type == 1:
            st.paragraph_format.widow_control = True
    footer = s.footer.paragraphs[0]
    footer.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    run = footer.add_run('Faiaz Dzhafarov  35553299  |  ')
    run.font.size = Pt(8)
    fld = OxmlElement('w:fldSimple'); fld.set(qn('w:instr'),'PAGE'); footer._p.append(fld)
    d.core_properties.author = 'Faiaz Dzhafarov'
    d.core_properties.title = 'Campus grocery store feasibility' + (' appendices' if appendix else '')
    d.core_properties.subject = 'BUS334 Assignment 3'
    for border in list(d.styles.element.xpath('.//w:pBdr')):
        border.getparent().remove(border)
    for border in list(d.element.xpath('.//w:pBdr')):
        border.getparent().remove(border)
    return d

def table(d, headers, values, widths, font=9.5):
    t = d.add_table(rows=1, cols=len(headers))
    t.alignment = WD_TABLE_ALIGNMENT.CENTER; t.autofit = False
    for i,w in enumerate(widths): t.columns[i].width = Cm(w)
    pr=t._tbl.tblPr
    borders=OxmlElement('w:tblBorders')
    for edge in ['top','left','bottom','right','insideH','insideV']:
        e=OxmlElement('w:'+edge); e.set(qn('w:val'),'single');e.set(qn('w:sz'),'4');e.set(qn('w:color'),'D9D9D9');borders.append(e)
    pr.append(borders)
    for i,h in enumerate(headers): t.rows[0].cells[i].text=h
    repeat=OxmlElement('w:tblHeader');t.rows[0]._tr.get_or_add_trPr().append(repeat)
    for row in values:
        c=t.add_row().cells
        for i,v in enumerate(row): c[i].text=str(v)
    for r,row in enumerate(t.rows):
        no_split=OxmlElement('w:cantSplit');row._tr.get_or_add_trPr().append(no_split)
        for c,cell in enumerate(row.cells):
            cell.width=Cm(widths[c]); cell.vertical_alignment=WD_CELL_VERTICAL_ALIGNMENT.CENTER
            tcpr=cell._tc.get_or_add_tcPr(); margin=OxmlElement('w:tcMar')
            for edge in ['top','bottom','left','right']:
                e=OxmlElement('w:'+edge);e.set(qn('w:w'),'65' if edge in ['top','bottom'] else '75');e.set(qn('w:type'),'dxa');margin.append(e)
            tcpr.append(margin)
            shade(cell,'DCE6ED' if r==0 else ('F5F7F9' if r%2==0 else 'FFFFFF'))
            for p in cell.paragraphs:
                p.paragraph_format.space_after=Pt(0);p.paragraph_format.line_spacing=1.05
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT if c==0 else WD_ALIGN_PARAGRAPH.CENTER
                for run in p.runs:run.font.size=Pt(font);run.bold=(r==0)
    d.add_paragraph().paragraph_format.space_after=Pt(0)
    return t

d = document()
for i,page in enumerate(PAGES):
    if i: d.add_page_break()
    for kind,value in page:
        if kind=='title': d.add_paragraph(value,'Title')
        elif kind=='subtitle': d.add_paragraph(value,'Subtitle')
        elif kind=='meta':
            p=d.add_paragraph(value);p.paragraph_format.space_after=Pt(8)
            for r in p.runs:r.font.size=Pt(9)
        elif kind in ['h1','h2']: d.add_heading(value,level=1 if kind=='h1' else 2)
        elif kind in ['p','source']:
            p=d.add_paragraph(value)
            if kind=='source':
                for r in p.runs:r.font.size=Pt(9)
                p.paragraph_format.line_spacing=1.1
        elif kind=='caption': d.add_paragraph(value,'Caption')
        elif kind=='figure':
            name,height=value
            p=d.add_paragraph();p.paragraph_format.space_after=Pt(3);p.paragraph_format.line_spacing=1
            p.paragraph_format.keep_with_next=True
            r=p.add_run();pic=r.add_picture(str(CHARTS/name),width=Cm(17.4),height=Inches(height))
            pic._inline.docPr.set('descr', name.replace('_',' ').replace('.png','')+'; counts and percentages from 22 respondents')
        elif kind=='profile':
            table(d,['Profile','Number and share'],[
                ('Study level','Undergraduate 15 (68.2%); postgraduate 7 (31.8%)'),
                ('Gender','Male 10 (45.5%); female 11 (50.0%); not stated 1 (4.5%)'),
                ('Ethnic group','South Asian 12 (54.5%); other 9 (40.9%); not stated 1 (4.5%)'),
                ('Living arrangement','Renting 9 (40.9%); family 8 (36.4%); accommodation 5 (22.7%)'),
                ('Campus days per week','Two days 4 (18.2%); three 11 (50.0%); four 7 (31.8%)')
            ],[3.3,14.1],9)
report=BASE/'35553299_Dzhafarov_BUS334_A3_Report.docx';d.save(report)

a=document(True)
a.add_paragraph('Campus grocery store survey appendices','Title')
a.add_paragraph('Faiaz Dzhafarov  35553299  BUS334 Assignment 3  18 October 2026')
a.add_heading('Appendix A  Questionnaire and coding key',1)
a.add_paragraph('All 20 questions were required. The following wording and option order match the questionnaire used for collection. Each option has an analysis code followed by its count out of 22 respondents. Codes were added for this appendix and were not shown in the live form. The main report is a separate five-page document.')
for i,q in enumerate(QUESTIONS):
    if i in [5,10,15]:
        a.add_page_break();a.add_heading('Appendix A  Questionnaire and coding key continued',1)
    a.add_heading(q['question'],2)
    if q['type']=='text':
        a.add_paragraph('Open text response. All 22 answers appear in Appendix C.')
    else:
        opts=q['options']
        text='; '.join(f"{j} = {o['label']} (n = {o['count']})" for j,o in enumerate(opts,1))+'.'
        p=a.add_paragraph(text)
        p.paragraph_format.space_after=Pt(8)
        if q['type']=='checkbox':
            p=a.add_paragraph('Multiple selections allowed. A cell containing two codes retains both selections.')
            for r in p.runs:r.italic=True;r.font.size=Pt(9)

codes=[]
for row in ROWS:
    coded=[]
    for i,q in enumerate(QUESTIONS[:19],1):
        opts=[o['label'] for o in q['options']]
        values=row[i].split(';') if q['type']=='checkbox' else [row[i]]
        code=[opts.index(v)+1 for v in values]
        assert [opts[c-1] for c in code]==values
        coded.append(','.join(map(str,code)))
    codes.append(coded)
for lo,hi in [(0,10),(10,19)]:
    a.add_page_break();a.add_heading('Appendix B  Individual response records',1)
    a.add_paragraph(f'Questions {lo+1} to {hi}. R01 to R22 follow the original CSV row order. Codes refer to Appendix A; commas within a cell indicate multiple selections. No response has been removed or replaced.')
    if lo==0:
        a.add_paragraph('All timestamps are 18 October 2026, GMT+4. The time column preserves the exported time to the second.')
        vals=[]
        for i,r in enumerate(ROWS):
            rawtime=r[0].split(' ',1)[1].replace(' GMT+4','')
            vals.append([f'R{i+1:02}',rawtime]+codes[i][lo:hi])
        table(a,['ID','Time']+[f'Q{j+1}' for j in range(lo,hi)],vals,[1,2.4]+[1.4]*10,9)
    else:
        vals=[[f'R{i+1:02}']+c[lo:hi] for i,c in enumerate(codes)]
        table(a,['ID']+[f'Q{j+1}' for j in range(lo,hi)],vals,[1.2]+[1.8]*9,9.5)
    a.add_paragraph('Original evidence: Google_Forms_Responses_2026-10-18.csv, supplied with this appendix. It contains the original wording, timestamps and all 22 complete answer records. The tables above are a readable coded presentation of those records.')

price_ids=[1,2,4,5,6,7,8,11,14,17,19,20,22]
for offset in [0,11]:
    a.add_page_break();a.add_heading('Appendix C  Open answers',1)
    if offset==0:
        a.add_paragraph('Question 20 asked why respondents would or would not shop at a grocery store on campus. Answers below are reproduced verbatim. For the price theme, I counted only explicit references to prices, fair or reasonable pricing, affordability, or being more expensive. The 13 coded records are R01, R02, R04, R05, R06, R07, R08, R11, R14, R17, R19, R20 and R22. Themes may overlap; this is a descriptive reading, not a separate survey measure.')
    else:a.add_paragraph('Question 20 continued. Response IDs match Appendix B and the source CSV row order.')
    table(a,['ID','Original answer'],[[f'R{i+1:02}',ROWS[i][20]] for i in range(offset,min(offset+11,N))],[1.1,16.3],10)
    # Narrative answer column stays left aligned.
    for row in a.tables[-1].rows:
        for p in row.cells[1].paragraphs:p.alignment=WD_ALIGN_PARAGRAPH.LEFT
appendix=BASE/'35553299_Dzhafarov_BUS334_A3_Appendices.docx';a.save(appendix)

alltext='\n'.join(value for page in PAGES for kind,value in page if kind in ['p','source'])
assert '\u2014' not in alltext and '\u2013' not in alltext
analysis={
    'source_csv_sha256':hashlib.sha256(RAW.read_bytes()).hexdigest(),
    'response_count':N,'main_report_pages_planned':5,'line_spacing':1.5,
    'all_coded_records_round_trip_to_original_answers':True,
    'open_price_theme':{'count':len(price_ids),'respondent_ids':price_ids,'method':'Explicit reference to price, affordability, fair/reasonable pricing or being more expensive. Verbatim answers retained.'},
    'undergraduate_positive_intention':{'positive':12,'n':15,'percent':80.0},
    'postgraduate_positive_intention':{'positive':4,'n':7,'percent':57.1},
    'response_rate':None,'response_rate_reason':'Unknown total group reach and overlap with personal invitations',
    'completion_rate_percent':100,
    'questionnaire_unchanged':True,'responses_unchanged':True,'submission_performed':False,
    'team_approval':'not confirmed; no claim of approval in report',
    'source_documents':['BUS334 Assignment 3 Summary.pdf','BUS334_Assignment 3 [Data Collection]_Marking Guide.pdf','Unit Outline section 4.2.3'],
    'rubric_coverage':{
        'Summary':'Page 1 topic, method, sample, response rate and conditional conclusion',
        'Results':'Pages 1 to 4 sample, completeness, descriptive counts, three figures, subgroup comparison and open answers',
        'Conclusion and recommendations':'Page 5 product range, pricing, trial measurement and research improvements tied to results',
        'Data and structure':'22 complete records, all three parts, appendices with full questionnaire and individual responses, original CSV',
        'Organisation presentation English':'Five pages, 1.5 body spacing, consistent headings, legible charts, simple academic English',
        'Quality':'Convenience sampling, unknown response rate, multiple-response denominators, limits on causal and financial claims',
        'Usability':'Product, price, format, promotion and further feasibility decisions; limitations made explicit'}
}
(BASE/'ANALYSIS_AND_RUBRIC_CHECK.json').write_text(json.dumps(analysis,ensure_ascii=False,indent=2)+'\n')
(BASE/'Source'/'report_content.json').write_text(json.dumps(PAGES,ensure_ascii=False,indent=2)+'\n')
print(report);print(appendix)
