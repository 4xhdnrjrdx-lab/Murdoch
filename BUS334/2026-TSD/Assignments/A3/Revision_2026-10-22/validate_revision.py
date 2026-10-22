"""Check the revised artifacts against the preserved response export."""
from pathlib import Path
from collections import Counter
from datetime import datetime
from zoneinfo import ZoneInfo
import csv, hashlib, json, re, zipfile
from docx import Document
from pypdf import PdfReader

B = Path(__file__).resolve().parent
A3 = B.parent
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def norm(s): return ' '.join(s.split())
def save(name, value): (B/name).write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n')
raw = A3/'Responses_2026-10-18/Google_Forms_Responses_2026-10-18.csv'
assert sha(raw) == 'b1abab5b724541cde709c1334edeb7bf7fbb550fe5d4a0b0c715b84afb6326f3'
headers, *rows = list(csv.reader(raw.open(encoding='utf-8-sig')))
questions = json.loads((raw.parent/'SUMMARY.json').read_text())['questions']
analysis = json.loads((B/'ANALYSIS.json').read_text())
assert len(rows)==22 and all(len(r)==21 and all(r) for r in rows)
report = Document(B/'35553299_Dzhafarov_BUS334_A3_Report_Revised.docx')
appendix = Document(B/'35553299_Dzhafarov_BUS334_A3_Appendices_Revised.docx')
assert report.styles['Normal'].paragraph_format.line_spacing == 1.5
assert report.styles['Normal'].font.size.pt == 11
assert report.styles['Normal'].font.name == 'Arial'
assert len(report.inline_shapes)==3
report_text = '\n'.join(p.text for p in report.paragraphs)
assert not re.search(r'\b(I|my|me|our|we)\b', report_text, re.I)
for text in ['Part 1  Summary', 'Part 2  Results', 'Conclusions', 'Recommendations and next steps', 'Limitations and further research']:
    assert text in report_text
assert 'accompanying CSV' not in report_text
assert 'Telegram' in report_text and 'WhatsApp' in report_text
assert 'response rate could not be calculated' in report_text
assert 'completion rate of 100%' in report_text
assert len(appendix.tables)==23
for i, q in enumerate(questions, 1):
    assert q['question']==headers[i]
    assert q['question'] in [p.text for p in appendix.paragraphs]
    if q['type']=='text': continue
    counts=Counter(v for r in rows for v in (r[i].split(';') if q['type']=='checkbox' else [r[i]]))
    t=appendix.tables[i-1]
    assert len(t.rows)==len(q['options'])+1
    for o, row in zip(q['options'],t.rows[1:]):
        assert [c.text for c in row.cells]==[o['label'],str(counts[o['label']]),f"{counts[o['label']]/22:.1%}"]
    if q['type']!='checkbox': assert sum(counts.values())==22
    for o in q['options']:
        assert any(p.text.endswith(o['label']) for p in appendix.paragraphs)
answers=[row.cells[1].text for t in appendix.tables[-2:] for row in t.rows[1:]]
assert answers == [r[20] for r in rows]
for i, r in enumerate(analysis['open_response_assignments'],1):
    assert r['answer']==rows[i-1][20]
    assert r['themes']==[t['code'] for t in analysis['open_answer_coding'] if i in t['ids']]
for t in analysis['open_answer_coding']:
    assert len(t['ids'])==t['count'] and round(t['count']/22*100,1)==t['percent']
for c in analysis['exploratory_crosstab']:
    group=[r for r in rows if r[5]==c['campus_days']]
    assert len(group)==c['n']
    assert sum(r[9].startswith(('4','5')) for r in group)==c['positive']
    assert round(c['positive']/c['n']*100,1)==c['percent']
chart_counts={8:[0,4,11,7,0],9:[0,0,6,11,5],12:[15,8,0,0],11:[6,13,3,0],10:[0,8,7,7,0],17:[15,3,1,0,3],19:[15,4,3,0,0,0]}
for n, counts in chart_counts.items(): assert counts==[o['count'] for o in questions[n-1]['options']]
shot=B/'Evidence/2026-10-22_google_forms_22_responses.png'
assert sha(shot)==analysis['screenshot_sha256']
with zipfile.ZipFile(B/'35553299_Dzhafarov_BUS334_A3_Appendices_Revised.docx') as z:
    assert shot.read_bytes() in [z.read(n) for n in z.namelist() if n.startswith('word/media/')]
pages={}
for stem, expected in [('Report',5),('Appendices',13)]:
    p=B/f'35553299_Dzhafarov_BUS334_A3_{stem}_Revised.pdf'
    pdf=PdfReader(p); assert len(pdf.pages)==expected
    for page in pdf.pages:
        text=page.extract_text()
        assert len(text)>150
        assert not re.search(r'\b(TODO|TBD|PLACEHOLDER|ChatGPT|OpenAI)\b',text,re.I)
    pages[stem]=expected
preserved={
 'Report_2026-10-18/35553299_Dzhafarov_BUS334_A3_Report.pdf':'3d2341ea7ab05f855c4ce4718cc6c8f5713f1a82853032921ee8cee80dcffd24',
 'Report_2026-10-18/35553299_Dzhafarov_BUS334_A3_Appendices.pdf':'b70594e5b391e347d5ebe02cc9aa9e6a3639df0ed9681ffcd20e78f2802f0e4e',
 'CSV_Replacement_2026-10-21/35553299_Dzhafarov_BUS334_A3_Original_Responses.pdf':'c288ea8d73794e71c6ffd7d493e66fd70b0e16f7c9ef84e1ae11f9dee731f931'}
for name, expected in preserved.items(): assert sha(A3/name)==expected
qa={
 'checked_at':datetime.now(ZoneInfo('Asia/Dubai')).isoformat(timespec='seconds'),
 'pages':pages, 'report_body_font':'Arial 11', 'report_body_line_spacing':1.5,
 'figures':3, 'closed_question_distributions_reconciled':19,
 'all_20_question_headers_and_options_preserved':True,
 'all_22_open_answers_verbatim':True, 'chart_counts_reconciled':True,
 'crosstab_recalculated_from_raw':True, 'theme_assignments_and_percentages_reconciled':True,
 'original_screenshot_embedded_without_editing':True,
 'source_csv_sha256':sha(raw), 'historical_submitted_pdfs_unchanged':preserved,
 'no_first_person_in_report_prose':True, 'no_placeholders_in_product_pdfs':True,
 'visual_review':{'report_pages':list(range(1,6)),'appendix_pages':list(range(1,14)),
 'method':'All final render-2 page PNGs inspected at full page size; no clipping, overlapping text, blank pages or split question tables. Charts, captions and verbatim answer rows were readable.'},
 'source_limits':['Anonymous identities not independently verified','Unknown invitation reach and overlap; no invitation response rate','Small convenience sample','Original checkbox priority wording and incomplete Q18 retained and disclosed'],
 'group_agreement_source':'User confirmation on 22 October 2026; no staff questionnaire approval claimed',
 'moodle_new_revision_submitted':False,
 'artifacts':[{ 'name':p.name,'bytes':p.stat().st_size,'sha256':sha(p)} for p in sorted(B.iterdir()) if p.suffix in ['.docx','.pdf']]
}
save('QA.json',qa)
print(json.dumps({'result':'PASS','pages':pages,'distributions':19,'open_answers':22},ensure_ascii=False))
