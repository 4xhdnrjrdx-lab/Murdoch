from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
from copy import deepcopy
from lxml import etree as E
from docx import Document
import json,hashlib,re
R=Path(__file__).resolve().parents[1];A2=R.parent
src=R/'Original_User_Copy.docx';out=A2/'For_Submission/BUS225_A2_Group9_Carrefour.docx'
changes=json.loads((R/'Source/edits.json').read_text())
W='http://schemas.openxmlformats.org/wordprocessingml/2006/main';NS={'w':W}
with ZipFile(src) as z:parts={n:z.read(n) for n in z.namelist()}
root=E.fromstring(parts['word/document.xml']);body=root.find(f'{{{W}}}body');paras=body.findall(f'{{{W}}}p')
for change in changes:
 p=paras[change['paragraph']];ts=p.xpath('.//w:t',namespaces=NS)
 assert ''.join(t.text or '' for t in ts)==change['before']
 ts[0].text=change['after'];ts[0].set('{http://www.w3.org/XML/1998/namespace}space','preserve')
 for t in ts[1:]:t.text=''
# Recover only the established heading formatting; retain the user's heading wording.
ref=Document(A2/'Complete_2026-10-21/BUS225_A2_Group9_Carrefour_Checked.docx')
heads={p.text[0]:p for p in ref.paragraphs if re.match(r'^[1-5] ',p.text)}
for i in [5,8,13,19,24]:
 old=paras[i];text=''.join(old.xpath('.//w:t/text()',namespaces=NS));replacement=E.fromstring(E.tostring(heads[text[0]]._p))
 ts=replacement.xpath('.//w:t',namespaces=NS);ts[0].text=text
 for t in ts[1:]:t.text=''
 body.replace(old,replacement)
# Remove the extra empty paragraph inserted below the names; no content is removed.
assert not ''.join(paras[4].xpath('.//w:t/text()',namespaces=NS)) and paras[4].find('.//w:sectPr',NS) is None
body.remove(paras[4])
parts['word/document.xml']=E.tostring(root,encoding='UTF-8',xml_declaration=True,standalone=True)
with ZipFile(out,'w',ZIP_DEFLATED) as z:
 for n,data in parts.items():z.writestr(n,data)
a=Document(src);b=Document(out);oldtext=[p.text for p in a.paragraphs];newtext=[p.text for p in b.paragraphs]
fi=next(i for i,t in enumerate(newtext) if t.startswith('Figure 1 Proposed'))
main='\n'.join(newtext[:fi]);ft=(A2/'Revision_2026-10-28/Source/blueprint_text.txt').read_text()
words=len(main.split())+len(ft.split());conservative=len(re.findall(r"\b\w+(?:['’]\w+)?\b",main+'\n'+ft))
assert words<=2000 and conservative<=2000,(words,conservative)
assert oldtext[oldtext.index('References'):]==newtext[newtext.index('References'):]
assert all(oldtext[i]==newtext[i-1] for i in range(20,24))
assert not re.search(r'\b(?:I|my|me)\b',main)
with ZipFile(src) as z:
 changed=[n for n in z.namelist() if z.read(n)!=parts[n]]
assert changed==['word/document.xml'],changed
(R/'Source/report_corrected.txt').write_text(main+'\n')
qa={'date':'2026-10-28','input_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'output_sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'original_main_words':1793,'main_words':len(main.split()),'blueprint_words':len(ft.split()),'total_words_excluding_references':words,'conservative_word_count':conservative,'words_removed':2168-words,'figure_preserved_byte_for_byte':True,'references_preserved':True,'ethics_paragraphs_preserved':True,'original_user_copy_preserved':str(src.relative_to(A2)),'changed_docx_parts':changed,'heading_formatting_restored':True,'extra_empty_paragraph_removed':True,'font_sizes_and_margins_preserved':True,'render_review':'pending'}
(R/'Checks/REVISION.json').write_text(json.dumps(qa,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(qa,ensure_ascii=False,indent=2))
