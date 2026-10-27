from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED
import lxml.etree as E
r=Path('/private/tmp/bus230-alex-demo-20261027');z=ZipFile(r/'build/preserved-candidate.pptx');d={n:z.read(n) for n in z.namelist()};ns={'p':'http://schemas.openxmlformats.org/presentationml/2006/main','a':'http://schemas.openxmlformats.org/drawingml/2006/main'};ruri='http://schemas.openxmlformats.org/officeDocument/2006/relationships';s=E.fromstring(d['ppt/slides/slide25.xml']);pic=s.xpath('.//p:pic[p:nvPicPr/p:cNvPr[@id="18"]]',namespaces=ns)[0];cnv=pic.find('p:nvPicPr/p:cNvPr',ns)
for x in cnv.findall('a:hlinkClick',ns):cnv.remove(x)
nvpr=pic.find('p:nvPicPr/p:nvPr',ns);nvpr.clear();cnv.set('name','Alex practice demonstration, 36 seconds');
for x in s.findall('p:timing',ns):s.remove(x)
rid=pic.find('p:blipFill/a:blip',ns).get('{'+ruri+'}embed');rel=E.fromstring(d['ppt/slides/_rels/slide25.xml.rels'])
for x in rel:
 if x.get('Id')==rid:x.set('Target','../media/alex-demo-36s.gif')
d['ppt/media/alex-demo-36s.gif']=(r/'build/alex-fallback.gif').read_bytes();d['ppt/slides/slide25.xml']=E.tostring(s,xml_declaration=True,encoding='UTF-8',standalone=True);d['ppt/slides/_rels/slide25.xml.rels']=E.tostring(rel,xml_declaration=True,encoding='UTF-8',standalone=True)
ct=E.fromstring(d['[Content_Types].xml']);E.SubElement(ct,'{http://schemas.openxmlformats.org/package/2006/content-types}Default',Extension='gif',ContentType='image/gif');d['[Content_Types].xml']=E.tostring(ct,xml_declaration=True,encoding='UTF-8',standalone=True)
with ZipFile(r/'build/gif-candidate.pptx','w',ZIP_DEFLATED) as o:
 for n,b in d.items():o.writestr(n,b)
p=ns['p'];pr=E.fromstring(d['ppt/presentation.xml']);ids=pr.find('{'+p+'}sldIdLst');ids[:]=[ids[24]];d['ppt/presentation.xml']=E.tostring(pr,xml_declaration=True,encoding='UTF-8',standalone=True)
with ZipFile(r/'build/gif-preview.pptx','w',ZIP_DEFLATED) as o:
 for n,b in d.items():o.writestr(n,b)
