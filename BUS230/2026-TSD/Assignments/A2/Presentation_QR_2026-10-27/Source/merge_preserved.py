from pathlib import Path
from copy import deepcopy
from zipfile import ZipFile,ZIP_DEFLATED
import lxml.etree as E,json,posixpath,hashlib
root=Path('/private/tmp/bus230-qr-20261027');source=Path('/private/tmp/murdoch-bus230-scripts-20261027/BUS230/2026-TSD/Assignments/A2/Local_Snapshots_2026-10-27/BUS230Assessment2Class2Group4_2026-10-26_LOCAL_SNAPSHOT_2026-10-27.pptx')
a=ZipFile(source);b=ZipFile(root/'build/edited-roundtrip.pptx');payload={n:a.read(n) for n in a.namelist()}
ns={'p':'http://schemas.openxmlformats.org/presentationml/2006/main','a':'http://schemas.openxmlformats.org/drawingml/2006/main'}
rns={'r':'http://schemas.openxmlformats.org/package/2006/relationships'}
rel_path='ppt/slides/_rels/slide25.xml.rels';rels=E.fromstring(b.read(rel_path));oldrels=E.fromstring(a.read(rel_path));oldtargets={r.get('Type').rsplit('/',1)[-1]:r.get('Target') for r in oldrels}
new_parts=[]
for rel in rels:
 typ=rel.get('Type').rsplit('/',1)[-1]
 if typ in ['slideLayout','notesSlide']:rel.set('Target',oldtargets[typ])
 elif typ=='image':
  target=rel.get('Target');input_part=target.lstrip('/') if target.startswith('/') else posixpath.normpath('ppt/slides/'+target)
  data=b.read(input_part);part='ppt/media/bus230-game-qr-20261027.png';payload[part]=data;new_parts.append(part);rel.set('Target','../media/'+part.rsplit('/',1)[1])
 elif typ=='hyperlink':
  assert rel.get('Target')=='https://cedar-retail-adkar-demo.spicy-rhino-0802.chatgpt.site/' and rel.get('TargetMode')=='External'
 else:raise RuntimeError('Unexpected slide relationship '+typ)
payload['ppt/slides/slide25.xml']=b.read('ppt/slides/slide25.xml');payload[rel_path]=E.tostring(rels,xml_declaration=True,encoding='UTF-8',standalone=True)
for n in range(19,31):
 name=f'ppt/notesSlides/notesSlide{n}.xml';old=E.fromstring(a.read(name));new=E.fromstring(b.read(name));xpath='.//p:sp[p:nvSpPr/p:nvPr/p:ph[@type="body"]]/p:txBody';oldbody=old.xpath(xpath,namespaces=ns);newbody=new.xpath(xpath,namespaces=ns);assert len(oldbody)==len(newbody)==1
 oldbody[0].getparent().replace(oldbody[0],deepcopy(newbody[0]));payload[name]=E.tostring(old,xml_declaration=True,encoding='UTF-8',standalone=True)
ct=E.fromstring(payload['[Content_Types].xml']);cns='http://schemas.openxmlformats.org/package/2006/content-types'
if not any(x.get('Extension')=='png' for x in ct):E.SubElement(ct,'{'+cns+'}Default',Extension='png',ContentType='image/png')
payload['[Content_Types].xml']=E.tostring(ct,xml_declaration=True,encoding='UTF-8',standalone=True)
with ZipFile(root/'build/preserved-candidate.pptx','w',ZIP_DEFLATED) as out:
 for name,data in payload.items():out.writestr(name,data)
slide_unchanged=[];table_owners=[]
for n in range(1,31):
 name=f'ppt/slides/slide{n}.xml'
 if n!=25:assert payload[name]==a.read(name);slide_unchanged.append(n)
 if E.fromstring(payload[name]).xpath('.//a:tbl',namespaces=ns):table_owners.append(n)
for n in range(1,19):assert payload[f'ppt/notesSlides/notesSlide{n}.xml']==a.read(f'ppt/notesSlides/notesSlide{n}.xml')
(root/'build/Preservation.json').write_text(json.dumps({'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'unchanged_slide_xml':slide_unchanged,'changed_visible_slide':25,'changed_notes':list(range(19,31)),'source_notes_1_to_18_preserved':True,'masters_and_layouts_preserved':True,'native_table_owner_slides':table_owners,'new_media_parts':new_parts,'hyperlinks':[r.get('Target') for r in rels if r.get('Type').endswith('/hyperlink')]},indent=2)+'\n')
print('Preserved 29 slide XML parts, source masters/layouts, and notes 1–18; applied only slide 25 and Aram notes.')
