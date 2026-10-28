"""Reproduce the targeted A2 revision from the preserved Checked.docx."""
from pathlib import Path
from copy import deepcopy
from zipfile import ZipFile, ZIP_DEFLATED
import hashlib, json, re
from lxml import etree as E
from docx import Document

HERE = Path(__file__).resolve().parent
A2 = HERE.parents[1]
OLD = A2/'Complete_2026-10-21'
INPUT = OLD/'BUS225_A2_Group9_Carrefour_Checked.docx'
OUTPUT = A2/'For_Submission/BUS225_A2_Group9_Carrefour.docx'
assert hashlib.sha256(INPUT.read_bytes()).hexdigest() == '77e9c6b28cf77f80315504f66542f9b99d5c4a5edf394f833553d37c4043b63c'

# Retain the original figure geometry, type sizes, colours and all other cells.
b = json.loads((OLD/'Source/blueprint.json').read_text())
b['note'] = b['note'].replace('(n.d.)', '(2022)')
b['lanes'][1]['cells'][4] = 'Self-scan if used; check total; pay; keep receipt'
b['lanes'][2]['cells'][2] = '1 Tally scans; 3 Staff restock; 4 Verify shelf F2 W'
b['lanes'][3]['cells'][2] = '2 Check stock; assign task. 5 Close alert; update stock'
b['controls'][1] = 'F2 False availability: scan > stock check > restock > verify > update.'
b['stock_exception'] = 'F2 No stock: show unavailable; keep task open.'
(HERE/'blueprint.json').write_text(json.dumps(b,ensure_ascii=False,indent=2)+'\n')
code = (OLD/'Source/build_documents.py').read_text().split('# Combined Word report.')[0]
code = code.replace("b=json.loads((SRC/'blueprint.json').read_text());refs=json.loads((SRC/'references.json').read_text())", "b=json.loads((SRC/'blueprint.json').read_text())")
# Place numbered F2 steps on separate lines for unambiguous cross-lane sequencing.
code = code.replace("ls=wrap(cell,boxw-16,14)", "ls = (['1 Tally scans;', '3 Staff restock;', '4 Verify shelf', 'F2 W'] if (i,j)==(2,2) else ['2 Check stock;', 'assign task.', '5 Close alert;', 'update stock'] if (i,j)==(3,2) else wrap(cell,boxw-16,14))")
code = code.replace("block(8,589,b['legend']", "text(550,568,b['stock_exception'],13.4)\nblock(8,589,b['legend']")
(HERE/'build_blueprint.py').write_text(code)
exec(compile(code,str(HERE/'build_blueprint.py'),'exec'), {'__file__':str(HERE/'build_blueprint.py'),'__name__':'__main__'})

W='http://schemas.openxmlformats.org/wordprocessingml/2006/main'
R='http://schemas.openxmlformats.org/officeDocument/2006/relationships'
P='http://schemas.openxmlformats.org/package/2006/relationships'
NS={'w':W}
with ZipFile(INPUT) as z: parts={n:z.read(n) for n in z.namelist()}
root=E.fromstring(parts['word/document.xml'])
body=root.find(f'{{{W}}}body')
paras=body.findall(f'{{{W}}}p')
def plain(p):return ''.join(p.itertext()) if False else ''.join(p.xpath('.//w:t/text()',namespaces=NS))
def append_text(p,text):
 run=E.SubElement(p,f'{{{W}}}r');t=E.SubElement(run,f'{{{W}}}t');t.set('{http://www.w3.org/XML/1998/namespace}space','preserve');t.text=text

trend = ("Carrefour's examples extend automation to conversational advice. "
         'In a bakery study, recommendation effects varied by visit frequency (Song et al., 2024). '
         'Its remotely operated robot limits conclusions about autonomous performance.')
staff = ' Managers should audit rankings and workload weekly.'
# Append without rewriting any original prose or direct run formatting.
append_text(paras[11], ' '+trend)
append_text(paras[22], staff)

# Add one reference in its alphabetical position, preserving every original entry.
ref=E.Element(f'{{{W}}}p')
ref.append(deepcopy(paras[36].find(f'{{{W}}}pPr')))
append_text(ref,'Song, S., Baba, J., Okafuji, Y., Nakanishi, J., Yoshikawa, Y., & Ishiguro, H. (2024). New comer in the bakery store: A long-term exploratory study toward design of useful service robot applications. ')
run=E.SubElement(ref,f'{{{W}}}r');rp=E.SubElement(run,f'{{{W}}}rPr');E.SubElement(rp,f'{{{W}}}i');E.SubElement(run,f'{{{W}}}t').text='International Journal of Social Robotics, 16'
append_text(ref,'(9–10), 1901–1918. ')
rels=E.fromstring(parts['word/_rels/document.xml.rels'])
rid='rId'+str(1+max(int(x.get('Id')[3:]) for x in rels))
url='https://doi.org/10.1007/s12369-024-01119-z'
E.SubElement(rels,f'{{{P}}}Relationship',Id=rid,Type=R+'/hyperlink',Target=url,TargetMode='External')
h=E.SubElement(ref,f'{{{W}}}hyperlink');h.set(f'{{{R}}}id',rid)
run=E.SubElement(h,f'{{{W}}}r');rp=E.SubElement(run,f'{{{W}}}rPr');col=E.SubElement(rp,f'{{{W}}}color');col.set(f'{{{W}}}val','174E79');E.SubElement(run,f'{{{W}}}t').text=url
paras[38].addprevious(ref)
parts['word/document.xml']=E.tostring(root,encoding='UTF-8',xml_declaration=True,standalone=True)
parts['word/_rels/document.xml.rels']=E.tostring(rels,encoding='UTF-8',xml_declaration=True,standalone=True)
parts['word/media/image1.png']=(HERE/'service_blueprint.png').read_bytes()
# A one-point paragraph-spacing adjustment prevents a stranded final line.
styles=E.fromstring(parts['word/styles.xml'])
normal=styles.xpath('./w:style[w:name/@w:val="Normal"]',namespaces=NS)[0]
spacing=normal.find(f'{{{W}}}pPr/{{{W}}}spacing')
assert spacing.get(f'{{{W}}}after')=='140'
spacing.set(f'{{{W}}}after','120')
parts['word/styles.xml']=E.tostring(styles,encoding='UTF-8',xml_declaration=True,standalone=True)
with ZipFile(OUTPUT,'w',ZIP_DEFLATED) as z:
 for n,data in parts.items():z.writestr(n,data)

figure_text=[b['title'],b['subtitle'],*b['columns']]
for lane in b['lanes']:figure_text += [lane['label'],*lane['cells']]
figure_text += [*b['boundaries'],*b['links'],b['controls_title'],*b['controls'],b['stock_exception'],b['legend'],b['standards'],b['note']]
figure_text='\n'.join(figure_text)
(HERE/'blueprint_text.txt').write_text(figure_text+'\n')
new=Document(OUTPUT)
main='\n'.join(p.text for p in new.paragraphs[:29])
(HERE/'report_text.txt').write_text(main+'\n')
word_count=len(main.split())+len(figure_text.split())
assert word_count<=2000,word_count
changes=[]
for idx,addition in [(11,' '+trend),(22,staff)]:
 oldp=Document(INPUT).paragraphs[idx]
 assert new.paragraphs[idx].text==oldp.text+addition
 changes.append({'paragraph':idx,'addition':addition.strip()})
with ZipFile(INPUT) as z:
 changed=[n for n in z.namelist() if z.read(n)!=parts[n]]
assert set(changed)=={'word/document.xml','word/_rels/document.xml.rels','word/media/image1.png','word/styles.xml'}
oldroot=E.fromstring(ZipFile(INPUT).read('word/document.xml'))
oldparas=oldroot.find(f'{{{W}}}body').findall(f'{{{W}}}p')
# Original paragraphs, except precisely the two additions, remain byte-identical as XML.
for i,p in enumerate(oldparas):
 if i not in [11,22]:assert E.tostring(p)==E.tostring(paras[i]),i
qa={'date':'2026-10-28','input_sha256':hashlib.sha256(INPUT.read_bytes()).hexdigest(),'output_sha256':hashlib.sha256(OUTPUT.read_bytes()).hexdigest(),
    'main_words':len(main.split()),'blueprint_words':len(figure_text.split()),'total_words_excluding_references':word_count,
    'original_paragraphs_preserved':True,'additions':changes,'new_reference':plain(ref),'figure_changes':['Self-scanning added to customer actions at stage 5','F2 numbered across visible and backstage actions','F2 sequence and unavailable-stock branch made explicit'],
    'layout_adjustment':'Normal paragraph space after reduced from 7 pt to 6 pt; fonts, margins, headings and page numbering preserved','unchanged_docx_parts':len(parts)-4,'changed_docx_parts':changed,'original_references_preserved':True,'new_reference_position':'after Majid Al Futtaim, before Wirtz','render_review':'pending'}
(HERE.parent/'Checks/REVISION.json').write_text(json.dumps(qa,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'words':word_count,'main':len(main.split()),'figure':len(figure_text.split()),'output':str(OUTPUT)},indent=2))
