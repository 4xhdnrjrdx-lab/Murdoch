"""Re-run structural, numerical and export checks without changing deliverables."""
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
import json,re,hashlib,unicodedata,zipfile
from urllib.parse import unquote
from docx import Document
from docx.oxml.ns import qn
from pypdf import PdfReader
import content
from finance import build
ROOT=Path(__file__).resolve().parents[1]
file=ROOT/'35553299DzhafarovF-2-Final.docx';pdf=file.with_suffix('.pdf')
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
 lines=t.splitlines();clean.append('\n'.join(l for l in lines if l!='Taking noon to Jordan | The Levant Five' and l!=str(i+1)))
joined=norm('\n'.join(clean))
check('24 pages in final PDF',len(reader.pages)==24)
check('Disclaimer absent from PDF as requested by user after lecturer clarification',not re.search(r'\bdisclaimer\b|The information contained in this report is given in good faith', '\n'.join(texts), re.I))
check('Disclaimer absent from DOCX',not any(re.search(r'\bdisclaimer\b|The information contained in this report is given in good faith',p.text,re.I) for p in doc.paragraphs))
for section in doc.sections:
 check('All margins 2.5 cm',all(abs(getattr(section,a).cm-2.5)<.01 for a in ['top_margin','bottom_margin','left_margin','right_margin']))
check('Normal style is 1.5 spaced',doc.styles['Normal'].paragraph_format.line_spacing==1.5)
check('Body font 11 pt',doc.styles['Normal'].font.size.pt==11)
check('Table rows cannot split and repeat headers',all(t.rows[0]._tr.get_or_add_trPr().find(qn('w:tblHeader')) is not None and all(r._tr.get_or_add_trPr().find(qn('w:cantSplit')) is not None for r in t.rows) for t in doc.tables))
for heading,page in pm.items():
 check('Page map: '+heading,heading in ' '.join(texts[page-1].split()))
toc_titles=[title for title,_ in content.SECTIONS]+['Bibliography','Appendix A. Market and demand exhibits','Appendix B. Financial assumptions and exhibits','Appendix C. Implementation and risk controls']
for title in toc_titles:
 check('Contents page number: '+title,any(p.text==f'{title}\t{pm[title]}' for p in doc.paragraphs))
for heading,ps in content.SECTIONS:
 for sub,body in ps:
  for p in body.split('\n'):
   check('Main paragraph exported: '+p[:48],norm(p) in joined)
prose='\n'.join(h+'\n'+'\n'.join(sub+'\n'+body for sub,body in ps) for h,ps in content.SECTIONS)
check('No em dash, en dash or spaced hyphen in authored main prose',not re.search(r'[\u2013\u2014]|\s-\s',prose))
check('No draft or team-review labels in PDF',not re.search(r'\bDRAFT\b|TEAM REVIEW|for review by', '\n'.join(texts), re.I))
check('All five LMS names on cover',all(name in ' '.join(texts[0].split()) for name,_ in content.MEMBERS))
check('All five student IDs on cover',all(student_id in texts[0] for _,student_id in content.MEMBERS))
check('Secondary-source and no-primary-research note retained',norm(content.METHOD_NOTE) in norm(texts[1]))
blocked=re.compile(r'OpenAI|Codex|ChatGPT|\bartificial intelligence\b|\bgenerative AI\b|\bAI[- ](?:assisted|generated)\b|preparation disclosure',re.I)
check('No requested attribution wording remains in PDF text or metadata',not blocked.search('\n'.join(texts)+str(reader.metadata)))
with zipfile.ZipFile(file) as archive:
 check('No requested attribution wording remains in DOCX content, properties or relationships',not any(blocked.search(archive.read(n).decode('utf-8')) for n in archive.namelist() if n.endswith(('.xml','.rels'))))
check('No unresolved placeholders in report','...' not in '\n'.join(p.text for p in doc.paragraphs) and not re.search(r'\b(TODO|TBD|INSERT HERE)\b',joined))
urls={rel.target_ref for rel in doc.part.rels.values() if rel.reltype.endswith('/hyperlink')}
expected={url for _,url in content.REFERENCES if url}
check('Every bibliography URL is a DOCX hyperlink',urls==expected)
pdf_urls=set()
for page in reader.pages:
 for an in page.get('/Annots',[]):
  a=an.get_object().get('/A')
  if a and a.get('/URI'):pdf_urls.add(str(a['/URI']))
check('All bibliography hyperlinks survive PDF export (Unicode URI encoding normalised)',{unquote(u) for u in expected}<={unquote(u) for u in pdf_urls})
wc=json.loads((ROOT/'qa/word_count.json').read_text());check('Conservative count including references at or below 4000',wc['conservative_total_before_appendices']<=4000)
fin=build();saved=json.loads((ROOT/'financial_model.json').read_text());check('Saved financial model equals recomputed model',saved==fin)
rm=json.loads((ROOT/'qa/rubric_map.json').read_text());check('Rubric weights equal 100%',sum(x['weight_percent'] or 0 for x in rm['rows'])==100);check('30 rubric rows mapped',len(rm['rows'])==30)
check('Both deliverables smaller than 100 MiB',all(p.stat().st_size<100*1024*1024 for p in [file,pdf]))
result={'checked_at':datetime.now(ZoneInfo('Asia/Dubai')).isoformat(timespec='seconds'),'status':'PASS','package_checks':checks,'package_check_count':len(checks),'financial_check_count':len(fin['checks']),'financial_checks':fin['checks'],'word_count':wc,'pages':len(reader.pages),'bibliography_entries':len(content.REFERENCES),'hyperlink_targets_in_docx':len(expected),'hyperlink_targets_in_pdf':len(pdf_urls),'visual_review':json.loads((ROOT/'qa/visual_review.json').read_text()),'artifacts':[{ 'name':p.name,'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in [file,pdf]],'limitations':['This revision is a document edit, not evidence of submission or team approval.','Commercial budgets, demand, legal classification and funding are assumptions requiring review.','Current consolidated foreign-investment regulation was not retrieved; no ownership entitlement asserted.','Word-processor counts can vary; deterministic method is disclosed.']}
(ROOT/'qa/VERIFICATION.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print('PASS:',len(checks),'package checks;',len(fin['checks']),'financial checks;',len(reader.pages),'pages;',len(expected),'hyperlinks')
