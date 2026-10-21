from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED
import xml.etree.ElementTree as E

B=Path('/private/tmp/bus230-redesign-build')
NS={'p':'http://schemas.openxmlformats.org/presentationml/2006/main','a':'http://schemas.openxmlformats.org/drawingml/2006/main','r':'http://schemas.openxmlformats.org/officeDocument/2006/relationships'}
REL='http://schemas.openxmlformats.org/package/2006/relationships'
for k,v in NS.items():E.register_namespace(k,v)

def process(kind):
 p=B/(kind+'-draft.pptx')
 with ZipFile(p) as z:parts={n:z.read(n) for n in z.namelist()}
 question,answer,conclusion=(22,23,24) if kind=='full' else (4,5,6)
 links={question:{'decision-A':answer,'decision-B':answer,'decision-C':answer},answer:{'nav-scenario':question,'nav-conclusion':conclusion}}
 count=30 if kind=='full' else 6
 for n in range(1,count+1):
  sp=f'ppt/slides/slide{n}.xml';rp=f'ppt/slides/_rels/slide{n}.xml.rels';root=E.fromstring(parts[sp]);rels=E.fromstring(parts[rp])
  if kind=='full' and n>=25:root.set('show','0')
  for sh in root.findall('p:cSld/p:spTree/p:sp',NS):
   props=sh.find('p:nvSpPr/p:cNvPr',NS)
   if props is None:continue
   name=props.get('name');target=links.get(n,{}).get(name)
   if target:
    rid='rIdOfflineJump'+str(target)
    if not any(x.get('Id')==rid for x in rels):E.SubElement(rels,f'{{{REL}}}Relationship',{'Id':rid,'Type':NS['r']+'/slide','Target':f'slide{target}.xml'})
    # CT_NonVisualDrawingProps requires hlinkClick before extLst.
    click=E.Element(f"{{{NS['a']}}}hlinkClick",{f"{{{NS['r']}}}id":rid,'action':'ppaction://hlinksldjump','tooltip':'Show worked answer' if n==question else 'Go to slide'})
    props.insert(0,click)
  parts[sp]=E.tostring(root,encoding='utf-8',xml_declaration=True);parts[rp]=E.tostring(rels,encoding='utf-8',xml_declaration=True)
 with ZipFile(B/(kind+'-linked.pptx'),'w',ZIP_DEFLATED) as z:
  for n,b in parts.items():z.writestr(n,b)
 print(kind,'offline links:',sum(map(len,links.values())),'hidden appendix:',6 if kind=='full' else 0)

process('full');process('aram')
