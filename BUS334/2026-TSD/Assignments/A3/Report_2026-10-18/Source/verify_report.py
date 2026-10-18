from pathlib import Path
from collections import Counter
import csv, json, re, hashlib
from docx import Document
from pypdf import PdfReader
from lxml import etree

BASE=Path(__file__).resolve().parents[1]
RAW=BASE.parent/'Responses_2026-10-18/Google_Forms_Responses_2026-10-18.csv'
ROWS=list(csv.reader(RAW.open(encoding='utf-8-sig')))[1:]
S=json.loads((BASE.parent/'Responses_2026-10-18/SUMMARY.json').read_text())
expected={8:[0,4,11,7,0],9:[0,0,6,11,5],10:[0,8,7,7,0],11:[6,13,3,0],12:[15,8,0,0],17:[15,3,1,0,3],19:[15,4,3,0,0,0]}
for q,counts in expected.items():
    options=[x['label'] for x in S['questions'][q-1]['options']]
    actual=Counter(v for r in ROWS for v in (r[q].split(';') if q==12 else [r[q]]))
    assert [actual[o] for o in options]==counts,(q,actual)
report=Document(BASE/'35553299_Dzhafarov_BUS334_A3_Report.docx')
appendix=Document(BASE/'35553299_Dzhafarov_BUS334_A3_Appendices.docx')
ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
assert len(report.inline_shapes)==3
assert report.styles['Normal'].paragraph_format.line_spacing==1.5
assert not report.styles.element.xpath('.//w:pBdr')
assert not appendix.styles.element.xpath('.//w:pBdr')
assert len(appendix.tables)==4
for part,(lo,hi) in enumerate([(0,10),(10,19)]):
    t=appendix.tables[part]
    for i,row in enumerate(t.rows[1:]):
        cells=[c.text for c in row.cells]
        assert cells[0]==f'R{i+1:02}'
        coded=cells[2:] if lo==0 else cells[1:]
        for j,value in enumerate(coded,lo):
            q=S['questions'][j]
            opts=[o['label'] for o in q['options']]
            decoded=[opts[int(x)-1] for x in value.split(',')]
            raw=ROWS[i][j+1].split(';') if q['type']=='checkbox' else [ROWS[i][j+1]]
            assert decoded==raw,(i,j)
written=[]
for t in appendix.tables[2:]:
    written.extend(row.cells[1].text for row in t.rows[1:])
assert written==[r[20] for r in ROWS]
price_ids=[i+1 for i,r in enumerate(ROWS) if re.search(r'pric|afford|expensive',r[20],re.I)]
assert price_ids==[1,2,4,5,6,7,8,11,14,17,19,20,22]
for role,count,n in [('Undergraduate student',12,15),('Postgraduate student',4,7)]:
    rs=[r for r in ROWS if r[1]==role]
    assert len(rs)==n and sum(r[9].startswith(('4','5')) for r in rs)==count
rp=PdfReader('/private/tmp/bus334-report-render/35553299_Dzhafarov_BUS334_A3_Report.pdf')
ap=PdfReader('/private/tmp/bus334-appendix-render/35553299_Dzhafarov_BUS334_A3_Appendices.pdf')
assert len(rp.pages)==5 and len(ap.pages)==8
assert all(len(p.extract_text().split())>80 for p in list(rp.pages)+list(ap.pages))
text='\n'.join(p.text for p in report.paragraphs)
assert '\u2013' not in text and '\u2014' not in text
assert 'Telegram' in text and 'WhatsApp' in text and 'response rate is unknown' in text
assert not any(x in text.lower() for x in ['lorem ipsum','todo','insert chart','as an ai'])
qa={'main_report_pages':5,'appendix_pages':8,'main_body_line_spacing':1.5,
    'figures':3,'charts_reconciled_to_original_csv':True,
    'all_418_closed_answers_round_trip_to_original':True,
    'all_22_open_answers_verbatim':True,'subgroup_counts_reconciled':True,
    'open_price_theme_reconciled':True,'source_csv_unchanged_sha256':hashlib.sha256(RAW.read_bytes()).hexdigest(),
    'visual_review':{'report_pages':[1,2,3,4,5],'appendix_pages':[1,2,3,4,5,6,7,8],
                     'result':'Reviewed all final rendered PNG pages; no clipping, overlap or broken characters. Charts, table columns, captions and page breaks readable.'},
    'humanizer':{'skill':'/Users/king1/.agents/skills/humanizer/SKILL.md','requested_reference':'https://github.com/blader/humanizer',
                 'method':'Draft, editorial audit and final prose review. Plain academic English; facts and original participant quotations preserved. No detector result claimed.'},
    'open_requirement':'Team agreement on the shared questionnaire is not confirmed in the records; the report does not invent it.',
    'assignment_submitted':False}
(BASE/'QA.json').write_text(json.dumps(qa,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(qa,ensure_ascii=False,indent=2))
