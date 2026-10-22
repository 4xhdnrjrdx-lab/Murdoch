from pathlib import Path
import ast, csv, json, hashlib, os, re, shutil, subprocess
from collections import Counter
from datetime import datetime
from zoneinfo import ZoneInfo
from docx import Document
from docx.shared import Cm, Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from reportlab.graphics.shapes import Drawing, String, Rect, Line
from reportlab.graphics import renderPDF
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor

BASE = Path(__file__).resolve().parent
A3 = BASE.parent
RAW = A3/'Responses_2026-10-18/Google_Forms_Responses_2026-10-18.csv'
ORIGINAL = A3/'Report_2026-10-18'
SOURCE_HASH = 'b1abab5b724541cde709c1334edeb7bf7fbb550fe5d4a0b0c715b84afb6326f3'
assert hashlib.sha256(RAW.read_bytes()).hexdigest() == SOURCE_HASH
HEADERS, *ROWS = list(csv.reader(RAW.open(encoding='utf-8-sig')))
N = len(ROWS)
assert N == 22 and all(len(r) == 21 and all(r) for r in ROWS)
QUESTIONS = json.loads((A3/'Responses_2026-10-18/SUMMARY.json').read_text())['questions']
for i, q in enumerate(QUESTIONS, 1):
    assert q['question'] == HEADERS[i]
    if q['type'] != 'text':
        counts = Counter(v for row in ROWS for v in (row[i].split(';') if q['type']=='checkbox' else [row[i]]))
        assert counts == Counter({o['label']:o['count'] for o in q['options'] if o['count']})

# Preserve the original document's measured page and style system without executing
# its builder (which would overwrite the historical submitted versions).
old_tree = ast.parse((ORIGINAL/'Source/build_report.py').read_text())
old_helpers = ast.Module(body=[n for n in old_tree.body if isinstance(n, ast.FunctionDef) and n.name in ('shade','document','table')], type_ignores=[])
exec(compile(old_helpers, '<original document helpers>', 'exec'), globals())

THEMES = [
    dict(code='C', label='Convenience and timely access', ids=[1,2,3,4,5,6,8,9,10,12,13,15,16,18,20,21,22],
         rule='Explicit convenient, nearby or handy access; time saving, quick service, class breaks, busy periods or urgent use. General usefulness alone was not enough.'),
    dict(code='P', label='Price and affordability', ids=[1,2,4,5,6,7,8,11,14,17,19,20,22],
         rule='Explicit prices, affordability, fair or reasonable pricing, or comparison with prices outside campus.'),
    dict(code='F', label='Specific food or drink purchases', ids=[2,3,4,5,6,7,10,11,16,17,18],
         rule='Explicit lunch, meals, food, snacks or drinks as a reason to use the store. Generic essentials or options were not counted.'),
    dict(code='Q', label='Choice or freshness', ids=[7,17,19],
         rule='Explicit good choice or selection, or freshness. A general mention of food was not enough.'),
    dict(code='U', label='Forgotten or urgent items', ids=[9,15,21],
         rule='Explicit forgetting an item or needing the store in a pinch. A normal short break was not counted as an emergency.')
]
for t in THEMES:
    t['count'] = len(t['ids']); t['percent'] = round(t['count']/N*100,1)
    assert len(set(t['ids'])) == len(t['ids']) and all(1 <= i <= N for i in t['ids'])
CROSS = []
for label in ['2 days','3 days','4 days']:
    group=[r for r in ROWS if r[5]==label]
    pos=sum(r[9].startswith(('4','5')) for r in group)
    CROSS.append(dict(campus_days=label,n=len(group),positive=pos,percent=round(pos/len(group)*100,1)))
assert [r['positive'] for r in CROSS] == [1,8,7]

CHARTS = BASE/'Charts'; CHARTS.mkdir(exist_ok=True)
FONTCONFIG = Path('/private/tmp/bus334-revision-fontconfig'); (FONTCONFIG/'cache').mkdir(parents=True,exist_ok=True)
(FONTCONFIG/'fonts.conf').write_text('<?xml version="1.0"?><!DOCTYPE fontconfig SYSTEM "fonts.dtd"><fontconfig><dir>/System/Library/Fonts</dir><dir>/Library/Fonts</dir><cachedir>/private/tmp/bus334-revision-fontconfig/cache</cachedir></fontconfig>')
os.environ['FONTCONFIG_FILE'] = str(FONTCONFIG/'fonts.conf')
pdfmetrics.registerFont(TTFont('ChartArial','/System/Library/Fonts/Supplemental/Arial.ttf'))
pdfmetrics.registerFont(TTFont('ChartArialBold','/System/Library/Fonts/Supplemental/Arial Bold.ttf'))
BLUE='#355B78'; GRAY='#A4B6C3'
def panel(d,x,y,w,h,labels,values,title,highlight=None):
    left=101 if w < 300 else 135
    plot=w-left-43
    d.add(String(x,y+h-13,title,fontName='ChartArialBold',fontSize=10))
    top=y+h-38;bottom=y+25
    step=(top-bottom)/max(len(labels)-1,1)
    for tick in [0,25,50,75,100]:
        xx=x+left+plot*tick/100
        d.add(Line(xx,bottom-10,xx,top+9,strokeColor=HexColor('#E4E8EC'),strokeWidth=.4))
        d.add(String(xx,bottom-21,str(tick),textAnchor='middle',fontName='ChartArial',fontSize=7.8,fillColor=HexColor('#555555')))
    for i,(label,count) in enumerate(zip(labels,values)):
        yy=top-i*step;value=count/N*100
        d.add(String(x,yy-3,label,fontName='ChartArial',fontSize=8.8))
        d.add(Rect(x+left,yy-5,plot*value/100,10,fillColor=HexColor(BLUE if highlight is None or i in highlight else GRAY),strokeWidth=0))
        d.add(String(x+w,yy-3,f'{value:.1f}%',textAnchor='end',fontName='ChartArial',fontSize=8.6))
    d.add(String(x+left+plot/2,y-7,'Respondents (%)',textAnchor='middle',fontName='ChartArial',fontSize=8))
def chart(d,stem):
    path=CHARTS/(stem+'.pdf');renderPDF.drawToFile(d,str(path))
    subprocess.run(['/Users/king1/.cache/codex-runtimes/codex-primary-runtime/dependencies/bin/override/pdftoppm','-singlefile','-r','300','-png',str(path),str(CHARTS/stem)],check=True,capture_output=True)

d=Drawing(504,180)
panel(d,0,18,242,162,['Very dissatisfied','Dissatisfied','Neutral','Satisfied','Very satisfied'],[0,4,11,7,0],'Current satisfaction  Q8',[2])
panel(d,262,18,242,162,['Very unlikely','Unlikely','Neutral','Likely','Very likely'],[0,0,6,11,5],'Intention to shop  Q9',[3,4])
chart(d,'01_demand')
d=Drawing(504,244)
panel(d,0,142,242,102,['Snacks and drinks','Meals and fruit','Take home groceries','Care and stationery'],[15,8,0,0],'Products  Q12')
panel(d,262,142,242,102,['Below AED 10','AED 10 to 24.99','AED 25 to 49.99','AED 50 or more'],[6,13,3,0],'Expected spend  Q11')
panel(d,0,18,504,112,['5 or more per week','2 to 4 per week','Once per week','1 to 3 per month','Less than monthly'],[0,8,7,7,0],'Expected visits  Q10')
chart(d,'02_purchases')
d=Drawing(504,185)
panel(d,0,18,242,167,['Price','Product choice','Freshness','Opening hours','Quick checkout'],[15,3,1,0,3],'Choice factor  Q17',[0])
panel(d,262,18,242,167,['Higher prices','Limited choice','Long queues','Unsuitable hours','Current alternatives','Nothing'],[15,4,3,0,0,0],'Main barrier  Q19',[0])
chart(d,'03_price')

PAGES=[
[
('title','Campus grocery store feasibility'),
('subtitle','BUS334 Assignment 3  Data collection and preliminary analysis'),
('meta','Faiaz Dzhafarov  |  Student ID 35553299  |  22 October 2026'),
('h1','Part 1  Summary'),
('p','Preliminary support was found for a small grocery store at Murdoch University Dubai. Among 22 respondents, 72.7% were likely or very likely to shop there if suitable products were offered at prices similar to nearby shops. Price was selected as the main choice factor by 68.2%, and higher prices were identified as the main barrier by 68.2%. A limited trial of snacks, drinks and quick meals was therefore recommended. Permanent investment could not be justified from this survey alone because actual sales and operating costs were not measured.'),
('h1','Part 2  Results'),
('h2','Data collection and sample'),
('p','The agreed group questionnaire comprised 20 questions: 19 closed questions and one open question. For this individual report, 22 complete responses were collected through Google Forms on 18 October 2026. The link was shared in a private Telegram group of Russian-speaking Murdoch students and through approximately 10 direct WhatsApp invitations. The total number reached and the overlap between channels were unknown, so the invitation response rate could not be calculated.'),
('p','All 22 returned questionnaires were complete, giving a completion rate of 100% and exceeding the minimum of 15. No missing answers, invalid options or identical answer sets were found. All records were retained. Names and email addresses were not collected, so respondent identities could not be independently verified. A convenience sample was obtained, rather than a random sample of the university.'),
('profile',None),
('source','Source for all results: Google Forms export, 18 October 2026, n = 22. Appendix A reproduces the questionnaire, Appendix B shows the response overview, Appendix C reports all closed-question frequencies and Appendix D documents the open-answer coding. The separate Original Responses PDF preserves every submitted answer and timestamp.')
],
[
('h1','Part 2  Results continued'),
('h2','Current provision and potential use'),
('figure',('01_demand.png',2.45)),
('caption','Figure 1  Satisfaction with existing options and conditional intention to shop. Each panel reports a separate question; n = 22.'),
('interpret','Half of respondents were neutral about existing options, 18.2% were dissatisfied and 31.8% were satisfied. Nearby supermarkets or convenience stores were selected as a usual source by 40.9% (Q6), and 36.4% had left campus to buy items during the previous month (Q7). An opportunity for convenient purchases was suggested, although widespread dissatisfaction was not demonstrated.'),
('interpret','Positive intention was recorded for 72.7%, with 27.3% neutral and none unlikely. This interest depended on suitable products and comparable prices. Conversion of that interest into paid purchases should be measured during a pilot before sales could be forecast.'),
('h2','Exploratory comparison by campus attendance'),
('cross',None),
('caption','Table 1  Positive intention means likely or very likely in Q9. Percentages use the number in each attendance group, not all 22 respondents.'),
('p','Positive intention was higher in the groups attending more often. With groups of only four, 11 and seven, no university-wide or causal conclusion could be drawn. Actual pilot purchases should be compared across teaching days.')
],
[
('h1','Part 2  Results continued'),
('h2','Purchases and the store offer'),
('figure',('02_purchases.png',3.12)),
('caption','Figure 2  Proposed products, spending per visit and visit frequency; n = 22. Multiple product selections were allowed in Q12, so its percentages total more than 100%.'),
('interpret','Snacks and drinks were selected by 68.2%, and meals and fruit by 36.4%. Take home groceries and care or stationery items received no selections. Expected spending was concentrated at AED 10 to 24.99 (59.1%), and 68.2% expected at least weekly visits. A compact range was therefore more appropriate for a trial than broad supermarket stock. These were intentions, not observed spending or visits.'),
('offer',None),
('caption','Table 2  Leading responses on reasons, incentives, format and promotion; n = 22. Q13, Q15 and Q16 allowed multiple selections. Full distributions appear in Appendix C.'),
('interpret','The near-even format preferences supported testing a small counter with limited fresh food before making a larger investment. Social media and student groups should be tested through measured customer referrals.')
],
[
('h1','Part 2  Results continued'),
('h2','Price and barriers'),
('figure',('03_price.png',2.42)),
('caption','Figure 3  Main choice factor and main barrier; n = 22. The two groups of 68.2% were separate question results and need not contain the same respondents.'),
('interpret','Price sensitivity was reinforced by Q18: 95.5% selected AED 5.00 as their maximum for water priced at AED 5.00 nearby, and 4.5% selected less. No premium was accepted in that hypothetical comparison. Comparable prices should be tested before relying on a convenience premium. Any ID discount or meal bundle should be checked against the contribution remaining after variable costs.'),
('h2','Themes in the open answers'),
('themes',None),
('caption','Table 3  Q20 themes were coded once per respondent per theme. Each percentage equals the theme count divided by 22. Themes overlapped and were not expected to total 100%. Coding rules and all original answers appear in Appendix D.'),
('interpret','Convenience and timely access were mentioned by 77.3%, while price was mentioned by 59.1%. R08 stated, "Having a store nearby would save time, as long as it is not more expensive than outside." The comments linked interest to easy access and affordability, supporting a trial focused on short breaks. Product choice or freshness was also mentioned, but by a smaller share. The coding was a descriptive interpretation of these answers, not an additional survey question.')
],
[
('h1','Part 3  Preliminary conclusions next steps and recommendations'),
('h2','Conclusions'),
('p','A small campus store was considered worth testing, subject to affordable prices and suitable products. This conclusion was supported by conditional shopping intention, preferences for snacks and drinks, and the convenience and price themes. A permanent store was not established as financially feasible: costs, realised demand and repeat purchases remained unmeasured.'),
('h2','Recommendations and next steps'),
('p','A pilot with a compact snacks and drinks range and a small fresh-meal selection was recommended. Initial commitments to take home groceries or stationery should be limited. Supplier prices and campus operating costs should be obtained before setting prices. Tests of an ID discount or meal bundle were recommended, subject to an adequate contribution after variable costs. Promotion through social media and student groups was recommended.'),
('pilot',None),
('caption','Table 4  Proposed checks before a permanent commitment. Cost-based targets should be set before a pilot; no sales target or profit estimate was assumed from the survey.'),
('h2','Limitations and further research'),
('p','The sample contained 22 students recruited through a limited set of contacts. Its gender balance did not make it representative. Generalisation beyond these respondents was therefore limited. A future survey should reach different programmes, teaching days and student networks, with invitations counted so that a response rate could be calculated.'),
('p','Five questions used checkboxes despite asking for a MOST or MAIN choice. Q6, Q12, Q15 and Q16 recorded 23 selections each; all selections were retained and percentages were based on 22 people. Q18 ended with an incomplete phrase. Before further collection, that wording should be completed, single-choice fields should be used where one priority was required, and the questionnaire should be piloted. Hypothetical interest and coded themes should then be checked against actual sales.'),
('source','Research data: individual Google Forms export, 18 October 2026. The original responses were preserved separately; no response or collected question was retrospectively changed.')
]
]

def para(doc,text,kind='p'):
    p=doc.add_paragraph()
    if kind=='interpret':p.add_run('Interpretation and implication. ').bold=True
    p.add_run(text)
    if kind=='source':
        p.paragraph_format.line_spacing=1.1
        for r in p.runs:r.font.size=Pt(8.7)
    return p

def fix_table(t,left_columns=()):
    for row in t.rows:
        for i,c in enumerate(row.cells):
            if i in left_columns:
                for p in c.paragraphs:p.alignment=WD_ALIGN_PARAGRAPH.LEFT

def add_image(doc,path,width=17.4):
    p=doc.add_paragraph();p.paragraph_format.line_spacing=1;p.paragraph_format.space_after=Pt(3);p.paragraph_format.keep_with_next=True
    pic=p.add_run().add_picture(str(path),width=Cm(width));pic._inline.docPr.set('descr',Path(path).stem.replace('_',' '))
    return p

doc=document()
doc.core_properties.modified=datetime(2026,10,22,13,15)
for page_no,page in enumerate(PAGES):
    if page_no:doc.add_page_break()
    for kind,value in page:
        if kind in ('title','subtitle'):doc.add_paragraph(value,'Title' if kind=='title' else 'Subtitle')
        elif kind=='meta':
            p=doc.add_paragraph(value)
            for r in p.runs:r.font.size=Pt(9)
        elif kind in ('h1','h2'):doc.add_heading(value,1 if kind=='h1' else 2)
        elif kind in ('p','source','interpret'):para(doc,value,kind)
        elif kind=='caption':doc.add_paragraph(value,'Caption')
        elif kind=='figure':
            name,height=value
            p=doc.add_paragraph();p.paragraph_format.space_after=Pt(3);p.paragraph_format.line_spacing=1;p.paragraph_format.keep_with_next=True
            pic=p.add_run().add_picture(str(CHARTS/name),width=Cm(17.4));pic._inline.docPr.set('descr',name.replace('_',' ')+'; percentage of 22 respondents')
        elif kind=='profile':
            table(doc,['Profile','Distribution'],[
                ('Study level','Undergraduate 68.2%; postgraduate 31.8%'),
                ('Gender','Male 45.5%; female 50.0%; not stated 4.5%'),
                ('Ethnic group','South Asian 54.5%; other 40.9%; not stated 4.5%'),
                ('Living arrangement','Renting 40.9%; family 36.4%; accommodation 22.7%'),
                ('Campus days per week','Two days 18.2%; three 50.0%; four 31.8%')
            ],[3.7,13.7],9.5)
        elif kind=='cross':
            table(doc,['Campus attendance','Respondents','Positive intention'],[(r['campus_days'],r['n'],f"{r['percent']:.1f}%") for r in CROSS],[6.2,4.0,7.2],10)
        elif kind=='offer':
            t=table(doc,['Question','Leading responses'],[
                ('Reason Q13','Convenience 40.9%; emergency purchases 27.3%'),
                ('Incentive Q14','ID discount 50.0%; meal bundles 31.8%'),
                ('Format Q15','Mini-market 50.0%; kiosk 45.5%'),
                ('Promotion Q16','Social media 36.4%; student groups 31.8%')
            ],[3.7,13.7],9.7);fix_table(t,[1])
        elif kind=='themes':
            table(doc,['Theme','Respondents'],[(t['label'],f"{t['percent']:.1f}%") for t in THEMES],[13.2,4.2],10)
        elif kind=='pilot':
            t=table(doc,['Decision','What should be measured','Basis for continuing'],[
                ('Demand','Transactions, repeat visits and contribution','Contribution covers staffing and occupancy costs'),
                ('Range and price','Basket contribution and unsold fresh stock','Retain viable items and revise costly offers'),
                ('Promotion','Customer referrals by channel','Prioritise channels generating purchases')
            ],[3.0,7.0,7.4],9.4);fix_table(t,[1,2])
report=BASE/'35553299_Dzhafarov_BUS334_A3_Report_Revised.docx';doc.save(report)

a=document(True);a.core_properties.title='Campus grocery store survey appendices'
for batch in range(4):
    if batch:a.add_page_break()
    else:
        a.add_paragraph('Campus grocery store survey appendices','Title')
        a.add_paragraph('Faiaz Dzhafarov  35553299  BUS334 Assignment 3  22 October 2026')
    a.add_heading('Appendix A  Questionnaire as administered'+(' continued' if batch else ''),1)
    if batch==0:
        a.add_paragraph('Campus Grocery Store Feasibility Survey')
        a.add_paragraph('The group-agreed questionnaire is reproduced below without response counts. Wording, option order and response modes were retained as used for collection. All 20 questions were required.')
    for q in QUESTIONS[batch*5:batch*5+5]:
        a.add_heading(q['question'],2)
        if q['type']=='text':
            a.add_paragraph('Written response')
            a.add_paragraph('__________________________________________________________________')
        else:
            mode='Select all applicable options' if q['type']=='checkbox' else 'Select one option'
            p=a.add_paragraph(mode);p.paragraph_format.space_after=Pt(2)
            for r in p.runs:r.font.size=Pt(9)
            for o in q['options']:
                p=a.add_paragraph(('[ ] ' if q['type']=='checkbox' else '( ) ')+o['label'])
                p.paragraph_format.space_after=Pt(1);p.paragraph_format.line_spacing=1.05
    if batch==3:
        para(a,'Q18 ended at "the same" in the collected form. Multiple selection was enabled for Q6, Q12, Q13, Q15 and Q16 despite the priority wording. These features were retained here as evidence and were discussed as limitations in the report.','source')

a.add_page_break();a.add_heading('Appendix B  Google Forms response overview',1)
a.add_paragraph('The original response summary was captured on 22 October 2026. It showed 22 responses, matching the 22 records in the export collected on 18 October. The screenshot below was not edited.')
shot=BASE/'Evidence/2026-10-22_google_forms_22_responses.png'
assert shot.exists()
add_image(a,shot)
a.add_paragraph('Figure B1  Original Google Forms response overview. The interface displays 22 responses and the study-level distribution of 15 undergraduates and seven postgraduates.','Caption')
a.add_paragraph('All original wording, timestamps and individual answers are also preserved in the separate Original Responses PDF. The counts below were recalculated from that same export.')

for batch in range(5):
    a.add_page_break();a.add_heading('Appendix C  Closed question results'+(' continued' if batch else ''),1)
    if batch==0:a.add_paragraph('Counts and percentages use 22 respondents. Multiple selections were retained for checkbox questions; their percentages may exceed 100%. For the other questions the counts total 22. Rounding may cause a small difference from 100%.')
    for q in QUESTIONS[batch*4:min(batch*4+4,19)]:
        a.add_heading(q['question'],2)
        t=table(a,['Response option','Count','Respondents'],[(o['label'],o['count'],f"{o['count']/N:.1%}") for o in q['options']],[12.1,2.1,3.2],10)
        fix_table(t,[0])
        if q['type']=='checkbox':para(a,'Multiple response question. Percentages were based on respondents, not selections.','source')

a.add_page_break();a.add_heading('Appendix D  Open answer coding',1)
a.add_paragraph('Q20 was coded descriptively. Each response was read against the rules below and assigned at most once to each theme. Several themes could be assigned to the same response. Percentages were calculated as the number of respondents mentioning a theme divided by 22, multiplied by 100. These were analyst-assigned themes, not additional questionnaire options.')
t=table(a,['Code and theme','Inclusion rule'],[(t['code']+'  '+t['label'],t['rule']) for t in THEMES],[5.2,12.2],9.5);fix_table(t,[1])
table(a,['Theme code','Respondents','Percentage'],[(t['code'],t['count'],f"{t['percent']:.1f}%") for t in THEMES],[5.8,5.8,5.8],10)
a.add_paragraph('The full coding assignments are shown beside each unchanged written response on the next pages. C included urgent access; U identified the narrower forgotten-item or emergency theme. F identified a specific intended food or drink purchase, while Q required an explicit choice or freshness condition. The themes could therefore overlap.')
for offset in [0,11]:
    a.add_page_break();a.add_heading('Appendix D  Original open answers'+(' continued' if offset else ''),1)
    a.add_paragraph('Response IDs R01 to R22 follow the original export row order. Codes refer to the preceding page. Original answers were reproduced verbatim, including first-person wording used by respondents.')
    vals=[]
    for i in range(offset,min(offset+11,N)):
        vals.append([f'R{i+1:02}',ROWS[i][20],', '.join(t['code'] for t in THEMES if i+1 in t['ids'])])
    t=table(a,['ID','Original answer','Themes'],vals,[1.1,14.0,2.3],10);fix_table(t,[1])
appendix=BASE/'35553299_Dzhafarov_BUS334_A3_Appendices_Revised.docx';a.save(appendix)

content='\n'.join(v for page in PAGES for k,v in page if k in ('p','interpret','source'))
assert not re.search(r'\b(I|we|my|our)\b',content,re.I)
assert '\u2014' not in content and '\u2013' not in content
assert hashlib.sha256(RAW.read_bytes()).hexdigest()==SOURCE_HASH
analysis={'source_csv_sha256':SOURCE_HASH,'response_count':N,'all_19_closed_question_distributions_reconciled':True,'source_questions_and_answers_unchanged':True,'group_questionnaire_agreement':{'confirmed_by':'User reply 22 October 2026: Да, согласовали эту анкету','staff_approval_of_questionnaire_not_claimed':True},'open_answer_coding':THEMES,'open_response_assignments':[{'id':f'R{i+1:02}','answer':r[20],'themes':[t['code'] for t in THEMES if i+1 in t['ids']]} for i,r in enumerate(ROWS)],'exploratory_crosstab':CROSS,'no_first_person_in_report_prose':True,'research_process_described_in_past_passive':True,'no_population_or_causal_inference_from_crosstab':True,'response_rate':None,'response_rate_reason':'Unknown Telegram reach and channel overlap','completion_rate':1,'new_submission_performed':False,'screenshot_sha256':hashlib.sha256(shot.read_bytes()).hexdigest()}
(BASE/'ANALYSIS.json').write_text(json.dumps(analysis,ensure_ascii=False,indent=2)+'\n')
(BASE/'report_content.json').write_text(json.dumps(PAGES,ensure_ascii=False,indent=2)+'\n')
print(report);print(appendix)
