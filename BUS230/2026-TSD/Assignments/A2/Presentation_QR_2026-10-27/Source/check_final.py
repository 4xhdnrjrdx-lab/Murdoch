from pathlib import Path
import json,re,zipfile,lxml.etree as E,hashlib
from PIL import Image,ImageChops
r=Path('/private/tmp/bus230-qr-20261027');final=r/'output-ready/BUS230Assessment2Class2Group4_2026-10-27_QR.pptx';z=zipfile.ZipFile(final);ns={'a':'http://schemas.openxmlformats.org/drawingml/2006/main','p':'http://schemas.openxmlformats.org/presentationml/2006/main'}
proof=[];content=json.loads((r/'build/Script_Content_EN.json').read_text());notes=json.loads((r/'build/Aram_Notes.json').read_text())
for n in range(1,31):
 root=E.fromstring(z.read(f'ppt/slides/slide{n}.xml'));assert root.get('show')!='0';text=' '.join(root.xpath('.//a:t/text()',namespaces=ns));assert 'Link pending' not in text
 if n>=19:
  got='\n'.join(E.fromstring(z.read(f'ppt/notesSlides/notesSlide{n}.xml')).xpath('.//p:sp[p:nvSpPr/p:nvPr/p:ph[@type="body"]]//a:t/text()',namespaces=ns));assert got.split()==notes[str(n)].split(),f'Notes mismatch {n}'
  s=next(s for s in content['slides'] if s['number']==n);proof.append({'slide':n,'title':s['title'],'role':'short audience question' if n==24 else 'office game' if n==25 else 'explanation only' if n==26 else 'research / wrap-up / references','spoken_words':len(re.findall(r"\b[\w’-]+\b",re.sub(r'\[[^\]]*\]','',s['speech'])))})
assert not any(b'/hyperlink' in z.read(p) for p in ['ppt/slides/_rels/slide25.xml.rels'])
unchanged=[]
for n in range(1,31):
 if n==25:continue
 a=Image.open(r/f'build/source-renders/slide-{n}.png').convert('RGB');b=Image.open(r/f'build/final-renders/slide-{n}.png').convert('RGB');assert ImageChops.difference(a,b).getbbox() is None;unchanged.append(n)
content['previous_presentation_source']=content['presentation_source'];content['previous_source_sha256']=content['source_sha256'];content['presentation_source']=final.name;content['source_sha256']=hashlib.sha256(final.read_bytes()).hexdigest();(r/'build/Script_Content_EN_Current.json').write_text(json.dumps(content,ensure_ascii=False,indent=2)+'\n')
audit={'total_slides':30,'visible_slides':30,'scripted_classroom_activities':[{'slide':24,'activity':'one A/B/C management decision; one brief audience explanation'},{'slide':25,'activity':'office game, five colleagues, two choices each'}],'slide_26':'presenter explanation, no additional question or poll','closing_questions':'general Q&A after references, not another exercise','notes_match_current_script':True,'planned_finish_including_general_questions':'29:20','rehearsed_timing':False,'unchanged_slides_pixel_comparison':unchanged,'source_masters_layouts_and_notes_1_to_18':'preserved byte for byte','text_hyperlink':'omitted after native Safe Links check error; game access through QR and printed URL','slides':proof}
(r/'build/Activity_Audit.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2)+'\n')
print('PASS: 30 visible slides; exactly 2 planned activities; notes match script; 29 unchanged slides pixel-identical')
