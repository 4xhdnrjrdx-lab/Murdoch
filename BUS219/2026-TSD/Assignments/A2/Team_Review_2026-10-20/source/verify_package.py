"""Re-run structural, numerical and export checks without changing deliverables."""
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
import json,re,hashlib,unicodedata
from docx import Document
from docx.oxml.ns import qn
from pypdf import PdfReader
import content
from finance import build
ROOT=Path(__file__).resolve().parents[1]
file=ROOT/'35553299DzhafarovF-2-TeamReview.docx';pdf=file.with_suffix('.pdf')
doc=Document(file);reader=PdfReader(pdf);pm=json.loads((ROOT/'qa/page_map.json').read_text())
checks=[]
def check(name,ok):
 assert ok,name;checks.append(name)
def norm(s):
 s=unicodedata.normalize('NFKC',s).replace('\u00ad','')
 return re.sub(r'\s+','',s)
texts=[p.extract_text() for p in reader.pages]
clean=[]
for i,t in enumerate(texts):
 lines=t.splitlines();clean.append('\n'.join(l for l in lines if l!='Taking noon to Jordan | The Levant Five | Team review' and l!=str(i+1)))
joined=norm('\n'.join(clean))
check('27 pages in final PDF',len(reader.pages)==27)
check('Exact prescribed disclaimer in first internal PDF page',norm(content.DISCLAIMER) in norm(texts[1]))
check('Disclaimer preserved verbatim in DOCX',any(p.text==content.DISCLAIMER for p in doc.paragraphs))
for section in doc.sections:
 check('All margins 2.5 cm',all(abs(getattr(section,a).cm-2.5)<.01 for a in ['top_margin','bottom_margin','left_margin','right_margin']))
check('Normal style is 1.5 spaced',doc.styles['Normal'].paragraph_format.line_spacing==1.5)
check('Body font 11 pt',doc.styles['Normal'].font.size.pt==11)
check('Table rows cannot split and repeat headers',all(t.rows[0]._tr.get_or_add_trPr().find(qn('w:tblHeader')) is not None and all(r._tr.get_or_add_trPr().find(qn('w:cantSplit')) is not None for r in t.rows) for t in doc.tables))
for heading,page in pm.items():
 check('Page map: '+heading,heading in ' '.join(texts[page-1].split()))
for heading,ps in content.SECTIONS:
 for sub,body in ps:
  for p in body.split('\n'):
   check('Main paragraph exported: '+p[:48],norm(p) in joined)
prose='\n'.join(h+'\n'+'\n'.join(sub+'\n'+body for sub,body in ps) for h,ps in content.SECTIONS)
check('No em dash, en dash or spaced hyphen in authored main prose',not re.search(r'[\u2013\u2014]|\s-\s',prose))
check('No unresolved placeholders in report','...' not in '\n'.join(p.text for p in doc.paragraphs) and not re.search(r'\b(TODO|TBD|INSERT HERE)\b',joined))
urls={rel.target_ref for rel in doc.part.rels.values() if rel.reltype.endswith('/hyperlink')}
expected={url for _,url in content.REFERENCES if url}
check('Every bibliography URL is a DOCX hyperlink',urls==expected)
pdf_urls=set()
for page in reader.pages:
 for an in page.get('/Annots',[]):
  a=an.get_object().get('/A')
  if a and a.get('/URI'):pdf_urls.add(str(a['/URI']))
check('All bibliography hyperlinks survive PDF export',expected<=pdf_urls)
wc=json.loads((ROOT/'qa/word_count.json').read_text());check('Conservative count including references at or below 4000',wc['conservative_total_before_appendices']<=4000)
fin=build();saved=json.loads((ROOT/'financial_model.json').read_text());check('Saved financial model equals recomputed model',saved==fin)
rm=json.loads((ROOT/'qa/rubric_map.json').read_text());check('Rubric weights equal 100%',sum(x['weight_percent'] or 0 for x in rm['rows'])==100);check('30 rubric rows mapped',len(rm['rows'])==30)
check('Both deliverables smaller than 100 MiB',all(p.stat().st_size<100*1024*1024 for p in [file,pdf]))
result={'checked_at':datetime.now(ZoneInfo('Asia/Dubai')).isoformat(timespec='seconds'),'status':'PASS','package_checks':checks,'package_check_count':len(checks),'financial_check_count':len(fin['checks']),'financial_checks':fin['checks'],'word_count':wc,'pages':len(reader.pages),'bibliography_entries':len(content.REFERENCES),'hyperlink_targets_in_docx':len(expected),'hyperlink_targets_in_pdf':len(pdf_urls),'visual_review':{'reviewed_pages':list(range(1,28)),'method':'All 27 rendered pages visually inspected in paired images. Final changed pages 1, 6, 8, 9 and 14 re-inspected individually; remaining page pixels matched the inspected render.','findings':'No clipped text, overlapping content, split table rows or blank pages. Contents page locations checked. Sparse cover, disclaimer and contents pages are intentional.','repairs':['Removed isolated short final main-text page by changing body from 11.5 to 11 pt; retained 1.5 line spacing.','Corrected same-author APA suffixes and bibliography order.','Removed inherited decorative title border.']},'artifacts':[{ 'name':p.name,'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in [file,pdf]],'limitations':['This is a team-review draft, not an assessment submission.','Commercial budgets, demand, legal classification and funding are assumptions requiring review.','Current consolidated foreign-investment regulation was not retrieved; no ownership entitlement asserted.','Word-processor counts can vary; deterministic method is disclosed.']}
(ROOT/'qa/VERIFICATION.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print('PASS:',len(checks),'package checks;',len(fin['checks']),'financial checks;',len(reader.pages),'pages;',len(expected),'hyperlinks')
