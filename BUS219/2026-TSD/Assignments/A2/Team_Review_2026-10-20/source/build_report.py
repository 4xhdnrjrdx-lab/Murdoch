"""Build editable report. Dependencies: python-docx. Render and inspect separately.
Optional qa/page_map.json supplies verified PDF pages for the contents list.
"""
from pathlib import Path
import json, re
from docx import Document
from docx.shared import Cm, Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.opc.constants import RELATIONSHIP_TYPE as RT
import content as c
import exhibits as x
from finance import build
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'35553299DzhafarovF-2-TeamReview.docx'
f=build();(ROOT/'financial_model.json').write_text(json.dumps(f,indent=2)+'\n')
doc=Document();sec=doc.sections[0]
sec.page_width=Inches(8.5);sec.page_height=Inches(11)
sec.top_margin=sec.bottom_margin=sec.left_margin=sec.right_margin=Cm(2.5)
sec.header_distance=sec.footer_distance=Cm(1.1)
sec.different_first_page_header_footer=True
style=doc.styles['Normal'];style.font.name='Times New Roman';style.font.size=Pt(11)
style.paragraph_format.line_spacing=1.5;style.paragraph_format.space_after=Pt(5)
style.paragraph_format.widow_control=True
for name,size in [('Title',25),('Subtitle',15),('Heading 1',15),('Heading 2',12)]:
 st=doc.styles[name];st.font.name='Times New Roman';st.font.size=Pt(size);st.font.color.rgb=RGBColor.from_string('111111')
 st.paragraph_format.line_spacing=1.5;st.paragraph_format.space_before=Pt(12);st.paragraph_format.space_after=Pt(6)
 st.paragraph_format.keep_with_next=True
for name in ['Heading 1','Heading 2']:doc.styles[name].font.bold=True
footer=sec.footer.paragraphs[0];footer.alignment=WD_ALIGN_PARAGRAPH.CENTER
r=footer.add_run();field=OxmlElement('w:fldSimple');field.set(qn('w:instr'),'PAGE');r._r.addnext(field)
header=sec.header.paragraphs[0];header.text='Taking noon to Jordan | The Levant Five | Team review'
header.style='Normal';header.paragraph_format.space_after=Pt(0)
for r in header.runs:r.font.size=Pt(9);r.font.color.rgb=RGBColor.from_string('555555')
# Default language and portable styles.
lang=OxmlElement('w:lang');lang.set(qn('w:val'),'en-GB');style.element.get_or_add_rPr().append(lang)
settings=doc.settings.element
upd=OxmlElement('w:updateFields');upd.set(qn('w:val'),'true');settings.append(upd)

def p(text,style=None):
 pa=doc.add_paragraph(text,style)
 return pa

def h(text,level=1):return doc.add_heading(text,level)
def page():doc.add_page_break()
def small(text):
 pa=p(text)
 for r in pa.runs:r.font.size=Pt(10)
 return pa

def link(pa,url):
 hl=OxmlElement('w:hyperlink');hl.set(qn('r:id'),pa.part.relate_to(url,RT.HYPERLINK,is_external=True))
 run=OxmlElement('w:r');rp=OxmlElement('w:rPr');col=OxmlElement('w:color');col.set(qn('w:val'),'1C4E80');rp.append(col)
 # Permit safe wrapping without inserting characters into the target URL.
 run.append(rp);t=OxmlElement('w:t');t.text=url;run.append(t);hl.append(run);pa._p.append(hl)

def table(headers,rows,widths=None):
 tb=doc.add_table(rows=1,cols=len(headers));tb.alignment=WD_TABLE_ALIGNMENT.CENTER;tb.autofit=False
 total=6.53
 if widths is None:widths=[total/len(headers)]*len(headers)
 for col,w in zip(tb.columns,widths):col.width=Inches(w)
 for i,v in enumerate(headers):tb.rows[0].cells[i].text=str(v)
 for row in rows:
  cells=tb.add_row().cells
  for i,v in enumerate(row):cells[i].text=str(v)
 for ri,row in enumerate(tb.rows):
  trpr=row._tr.get_or_add_trPr();cant=OxmlElement('w:cantSplit');trpr.append(cant)
  if ri==0:
   rep=OxmlElement('w:tblHeader');trpr.append(rep)
  for ci,cell in enumerate(row.cells):
   cell.width=Inches(widths[ci]);cell.vertical_alignment=WD_CELL_VERTICAL_ALIGNMENT.CENTER
   tcpr=cell._tc.get_or_add_tcPr();margin=OxmlElement('w:tcMar')
   for edge in ['top','left','bottom','right']:
    el=OxmlElement('w:'+edge);el.set(qn('w:w'),'65' if edge in ['top','bottom'] else '90');el.set(qn('w:type'),'dxa');margin.append(el)
   tcpr.append(margin)
   bd=OxmlElement('w:tcBorders')
   for edge in ['top','left','bottom','right']:
    el=OxmlElement('w:'+edge);el.set(qn('w:val'),'single');el.set(qn('w:sz'),'4');el.set(qn('w:color'),'D0D0D0');bd.append(el)
   tcpr.append(bd)
   if ri==0:
    shade=OxmlElement('w:shd');shade.set(qn('w:fill'),'EDF1F5');tcpr.append(shade)
   for pa in cell.paragraphs:
    pa.paragraph_format.space_before=Pt(0);pa.paragraph_format.space_after=Pt(0);pa.paragraph_format.line_spacing=1.5
    pa.paragraph_format.keep_with_next=False
    for run in pa.runs:run.font.size=Pt(10);run.bold=ri==0
 p('')
 return tb

def num(v,dec=0):
 s=f'{abs(v):,.{dec}f}'
 return f'({s})' if v<0 else s

def financial_rows(labels):
 return [[label]+[num(a[key],dec) for a in f['annual']] for label,key,dec in labels]

# Cover; first internal page follows immediately.
p('BUS219 INTERNATIONAL BUSINESS','Subtitle')
p('Assignment 2 | Major Project Report')
p(c.TITLE,'Title');p(c.SUBTITLE,'Subtitle')
p('The Levant Five')
p('Aram • Faiaz Dzhafarov • Abdoul • Hatim • Denis')
p('Faiaz Dzhafarov | 35553299')
p('2026-TSD | Murdoch University Dubai')
p(c.DATE)
p('TEAM REVIEW DRAFT')
p('Prepared for discussion and verification. Not submitted.')
p('Report due: 6 November 2026, 19:55 Asia/Dubai')
page()
h('Disclaimer and preparation disclosure')
p(c.DISCLAIMER)
p(c.NOTICE)
p('Referencing: APA 7 author-date. Research cut-off: 20 October 2026. The calculations are illustrative project scenarios, not company information.')
page();h('Contents')
pm_path=ROOT/'qa/page_map.json';pm=json.loads(pm_path.read_text()) if pm_path.exists() else {}
toc_titles=[title for title,_ in c.SECTIONS]+['Bibliography','Appendix A. Market and demand exhibits','Appendix B. Financial assumptions and exhibits','Appendix C. Governance and team review']
for title in toc_titles:
 pa=p(f'{title}\t{pm.get(title,"...")}')
 pa.paragraph_format.tab_stops.add_tab_stop(Inches(6.35),WD_ALIGN_PARAGRAPH.RIGHT)
 pa.paragraph_format.space_after=Pt(1)
page()
for title,paras in c.SECTIONS:
 h(title)
 for sub,body in paras:
  if sub:h(sub,2)
  for text in body.split('\n'):p(text)
page();h('Bibliography')
small('APA 7 author-date style. Online sources were retrieved on 20 October 2026. Undated pages are identified as n.d.; access does not establish when their content was last updated.')
for title,url in c.REFERENCES:
 pa=p('')
 match=re.match(r'(.+?\([^)]+\)\. )(.*)',title)
 if match:
  pa.add_run(match.group(1));pa.add_run(match.group(2)).italic=True
 else:pa.add_run(title)
 pa.paragraph_format.left_indent=Cm(.65);pa.paragraph_format.first_line_indent=Cm(-.65)
 pa.paragraph_format.space_after=Pt(7)
 if url:pa.add_run(' ');link(pa,url)
page();h('Appendix A. Market and demand exhibits')
small('Exhibits 1 and 2 are the authoring assistant’s synthesis and scenario assumptions. Company and market evidence is cited in Sections 3 to 5; no primary customer research has been conducted.')
for idx,(title,headers,rows) in enumerate(x.APPENDIX_A):
 if idx==1:page()
 h(title,2);table(headers,rows, [1.55,2.45,2.53] if idx==0 else [2.8,1.24,1.24,1.25])
 if idx==2:small('Weighted basket = (40% × 50) + (35% × 40) + (25% × 44) = JOD 45. Order share differs from GMV share. 2027 order counts are 24,000, 21,000 and 15,000 respectively. Category mix is held constant in later years.')
page();h('Appendix B. Financial assumptions and exhibits')
small('Source for all financial exhibits: illustrative model financial_model.json and source/finance.py, prepared 20 October 2026. Currency: nominal Jordanian dinars (JOD). Parentheses indicate negative amounts. Rounding is for display only.')
for i,(title,body) in enumerate(x.ASSUMPTIONS):
 h(title,2);p(body)
page();h('Exhibit 3. Unit economics and fixed budgets',2)
table(['Per net completed order, JOD','2027','2028','2029'],[
['Goods GMV','45.00','45.00','45.00'],['Commission income, 15%','6.75','6.75','6.75'],['Delivery income','3.00','3.00','3.00'],['Net platform revenue','9.75','9.75','9.75'],['Payment / collection cost','0.90','0.90','0.90'],['Fulfilment and delivery','7.00','4.80','4.50'],['Extra handling / loss reserve','0.90','0.70','0.60'],['Contribution','0.95','3.35','3.75']], [3.2,1.11,1.11,1.11])
table(['Fixed cash expense, JOD','2027','2028','2029'],[
[label]+[num(v) for v in f['inputs'][key]] for label,key in [('Personnel','staff'),('Marketing','marketing'),('Platform support','platform_support'),('Rent, advisers and admin','rent_advisers_admin')]
]+[['Total fixed expense']+[num(a['fixed_cost']) for a in f['annual']]], [3.2,1.11,1.11,1.11])
small('Contribution = AOV × commission + net delivery fee − AOV × payment rate − logistics − extra handling/loss allowance. First-year setup expense of JOD 100,000 is additional. Initial personnel envelope: lead 36,000; operations 24,000; merchant manager 24,000; three service roles 20,000 each, including employer costs.')
page();h('Exhibit 4. Projected profit and loss',2)
table(['JOD unless stated','2027','2028','2029'],financial_rows([
('Net completed orders','orders',0),('Goods GMV, memorandum only','gmv',0),('Commission income','commission_revenue',0),('Delivery income','delivery_revenue',0),('Net platform revenue','revenue',0),('Payment / collection cost','payment_cost',0),('Fulfilment and delivery','logistics_cost',0),('Extra handling / loss reserve','handling_reserve',0),('Contribution','contribution',0),('Fixed operating expense','fixed_cost',0),('One-off setup expense','setup',0),('EBITDA','ebitda',0),('Depreciation','depreciation',0),('Operating profit (EBIT)','ebit',0),('Illustrative tax reserve','tax',0),('Net profit / (loss)','net_profit',0)]),[3.2,1.11,1.11,1.11])
small('EBITDA = contribution − fixed cash expense − setup expense. EBIT = EBITDA − depreciation. Net profit = EBIT − max(EBIT, 0) × 21%. No interest is assumed. GMV is shown only as an operating volume measure and is never added to revenue.')
page();h('Exhibit 5a. Annual cash flow',2)
table(['JOD','2027','2028','2029'],financial_rows([
('Opening cash','cash_opening',0),('Equity received','equity_injection',0),('EBITDA','ebitda',0),('Cash tax provision','tax',0),('Increase in net working capital','delta_nwc',0),('Operating cash flow','operating_cash_flow',0),('Capital expenditure','capex',0),('Free cash flow before funding','free_cash_flow',0),('Closing cash','cash_closing',0)]),[3.2,1.11,1.11,1.11])
h('Exhibit 5b. Simplified net-asset reconciliation',2)
table(['Year-end JOD','2027','2028','2029'],financial_rows([
('Cash','cash_closing',0),('Net operating working capital','nwc',0),('Equipment, net of depreciation','net_ppe',0),('Net assets','net_assets',0),('Paid equity','paid_equity',0),('Cumulative earnings / (losses)','retained_earnings',0),('Total equity','total_equity',0)]),[3.2,1.11,1.11,1.11])
small('Net assets equal equity in every year. This net presentation is an economic planning schedule, not a statutory balance sheet. Separate gross receivables, payables, tax accounts and safeguarded settlement balances require agreed contracts. Three-year free cash flow totals (361,400); funding is 900,000, leaving cash of 538,600.')
page();h('Exhibit 5c. Monthly cash control',2)
table(['2027 month','Net orders','Closing cash JOD'],[[str(m['month']),num(m['orders']),num(m['closing_cash'])] for m in f['monthly'][:12]],[1.5,2,3.03])
small('2027 contribution follows the monthly order schedule; fixed cost is JOD 25,000 each month. January includes funding 600,000, setup 100,000, capex 90,000 and working capital 40,000. The lowest month-end cash is December: 127,000. Figures do not test daily liquidity within a month.')
small('2028 assumes 12,500 orders each month; 2029 assumes 20,000. Funding, capex and working-capital increases occur in January, with tax provision spread monthly. All 36 months are retained in financial_model.json. Without the planned second funding tranche, January 2028 month-end cash would be (18,625), so expansion cannot proceed on annual totals alone.')
page();h('Exhibit 6. Break-even and sensitivity',2)
table(['2029 case','Orders','Contribution / order','EBIT JOD'],[[r['case'],num(r['orders']),num(r['contribution_per_order'],3),num(r['ebit'])] for r in f['sensitivity']],[2.8,1.1,1.33,1.3])
small('Base fixed cash cost = 540,000; depreciation = 70,000. Cash operating break-even = 540,000 ÷ 3.75 = 144,000 orders. Accounting break-even = (540,000 + 70,000) ÷ 3.75 = 162,666.67 orders, rounded upward to 162,667. Break-even excludes additional capex and working-capital funding.')
small('Combined downside: 180,000 orders, 12% commission and JOD 5.50 logistics per order. Other inputs remain unchanged. Sensitivities hold fixed costs constant and show 2029 operating profit, not a full multi-year recovery plan. Lower volume may also prevent the assumed logistics discount, making the combined case particularly relevant.')
small('No terminal value is used. Positive third-year earnings do not establish payback or investment value. Before approval, replace cost assumptions with bids, agree tax treatment, and test a rolling cash forecast under delayed funding and slower growth.')
page();h('Appendix C. Governance and team review')
h('Exhibit 7. Proposed operating controls',2)
table(['Risk','Trigger / review','Owner','Response'],x.RISK_ROWS,[1.5,1.35,1.15,2.53])
small('All thresholds and owners are proposed roles. No employees, advisers, partner contracts or investor commitments have been secured. Resolve decision authority and escalation arrangements before launch.')
page();h('Proposed academic review responsibilities',2)
table(['Member','Poster responsibility','Review required now'],x.TEAM_ROWS,[.8,2.6,3.13])
small('The poster records intended roles, not completed work. The group of five is permitted according to the user’s prior confirmation. Full names and IDs, topic approval, completed contributions, meeting minutes, signed charter and peer evaluation remain for the actual team to verify. Do not backfill invented records.')
page();h('Suggested review schedule and open decisions',2)
table(['Proposed checkpoint','Action'],x.SCHEDULE_ROWS,[1.7,4.83])
p('Expected difficulties are obtaining current legal guidance, dated logistics bids, defensible customer evidence and consistent contributions within the deadline. These are anticipated constraints, not events that have already happened.')
p('Decisions requiring agreement: retain the proposed retail scope; confirm topic approval and permitted AI use; select the uploader; challenge the sales, commission, logistics and funding assumptions; decide the evidence threshold for a JV. No topic change or external communication has been made.')
h('AI assistance and research record',2)
p('OpenAI Codex performed source discovery and review, financial modelling, drafting, language editing and document preparation. The humanizer instructions were applied for clarity and natural academic phrasing, without adding invented experience or concealing assistance. The team has not yet verified or approved the output.')
p('The original user prompt is retained as NEW_CHAT_PROMPT_RU.txt in the parent A2 folder. Editable content, calculations, source register, rubric mapping and QA notes accompany the report. This record is not a complete chat transcript. Preserve the relevant conversation and follow the lecturer’s disclosure requirements before submission.')

doc.core_properties.title=c.TITLE;doc.core_properties.subject='BUS219 Assignment 2 | Team review draft'
doc.core_properties.author='Prepared with OpenAI Codex for review by The Levant Five'
doc.core_properties.keywords='BUS219; noon; Jordan; feasibility; team review'
for container in [doc.element, doc.styles.element]:
 for border in list(container.iter(qn('w:pBdr'))):
  border.getparent().remove(border)
doc.save(OUT)
# Deterministic counting; full visible strings, including bibliography hyperlink text.
def words(t):return len(re.findall(r'\S+',t))
main='\n'.join(title+'\n'+'\n'.join(sub+'\n'+body for sub,body in paras) for title,paras in c.SECTIONS)
bib='Bibliography\nAPA 7 author-date style. Online sources were retrieved on 20 October 2026. Undated pages are identified as n.d.; access does not establish when their content was last updated.\n'+'\n'.join(t+' '+(u or '') for t,u in c.REFERENCES)
# Get XML text in actual document order, before the first Appendix A heading (not TOC entry).
texts=[]
for el in doc.element.body:
 ts=''.join(el.itertext()) if False else ''.join(el.xpath('.//w:t')) if False else ''.join(t.text or '' for t in el.iter(qn('w:t')))
 if ts=='Appendix A. Market and demand exhibits':break
 texts.append(ts)
pre='\n'.join(texts)
counts={'method':'Whitespace-delimited visible tokens. Includes headings, citations and each URL as a token; excludes headers, footers and appendix/exhibit text. Conservative total adds cover, disclaimer, contents and bibliography. Word processors may differ on punctuation.',
'main_including_headings':words(main),'bibliography_including_heading_note_urls':words(bib),'front_matter_and_contents':words(pre)-words(main)-words(bib),'conservative_total_before_appendices':words(pre),
'unit_outline_limit':4000,'references_excluded_from_limit':False}
(ROOT/'qa/word_count.json').write_text(json.dumps(counts,indent=2)+'\n')
(ROOT/'source/report_prose.txt').write_text(main+'\n\n'+bib+'\n')
print(json.dumps(counts,indent=2));print(OUT)
