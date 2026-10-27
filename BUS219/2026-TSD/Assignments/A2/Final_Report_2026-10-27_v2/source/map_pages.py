"""Extract page locations from rendered PDF. Rebuild DOCX once, then recheck stability."""
import sys,json,re
from pathlib import Path
from pypdf import PdfReader
import content
ROOT=Path(__file__).resolve().parents[1]
pdf=Path(sys.argv[1]);reader=PdfReader(pdf)
titles=[title for title,_ in content.SECTIONS]+[sub for _,ps in content.SECTIONS for sub,_ in ps if sub]+['Bibliography','Appendix A. Market and demand exhibits','Appendix B. Financial assumptions and exhibits','Appendix C. Implementation and risk controls','Exhibit 1. SWOT and response','Exhibit 2a. Customer and order assumptions','Exhibit 2b. Planned sales mix, 2027','Exhibit 3. Unit economics and fixed budgets','Exhibit 4. Projected profit and loss','Exhibit 5a. Annual cash flow','Exhibit 5b. Simplified net-asset reconciliation','Exhibit 5c. Monthly cash control','Exhibit 6. Break-even and sensitivity','Exhibit 7. Proposed operating controls']
page_map={}
for title in titles:
 hits=[]
 for i,p in enumerate(reader.pages):
  if i<2:continue
  txt=' '.join(p.extract_text().split())
  if title in txt:hits.append(i+1)
 assert len(hits)==1,(title,hits)
 page_map[title]=hits[0]
(ROOT/'qa/page_map.json').write_text(json.dumps(page_map,indent=2)+'\n')
print('Mapped',len(page_map),'headings across',len(reader.pages),'pages')
