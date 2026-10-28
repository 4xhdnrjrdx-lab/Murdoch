from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
from lxml import etree as E
from copy import deepcopy
import hashlib,json,re
R=Path(__file__).resolve().parents[1];A=R.parent
src=R/'Original_User_V2.docx';out=A/'For_Submission/BUS225_A2_Group9_Carrefour.docx'
assert hashlib.sha256(src.read_bytes()).hexdigest()=='36ff44a8b642537bc901940c3291c48b343fd6644b10d748dfc84a7fc0cddda0'
W='http://schemas.openxmlformats.org/wordprocessingml/2006/main'; ns={'w':W}
with ZipFile(src) as z:parts={n:z.read(n) for n in z.namelist()}
r=E.fromstring(parts['word/document.xml']);ps=r.findall('w:body/w:p',ns)
text=lambda p:''.join(p.xpath('.//w:t/text()',namespaces=ns))
before=[text(p) for p in ps]
changes={
10:[('In other UAE countries','Outside the UAE'),('Based on purchase history, Carrefour introduced the Brazil\'s Nutri Choice',"Carrefour introduced Brazil's Nutri Choice"),('nutritional and price comparisons','nutritional and price comparisons using purchase history'),('Both statements rule out','Neither statement confirms'),('do not rely on nutrition ratings','do not use nutrition ratings instead of checking ingredients')],
11:[('Wirtz et al (2018)','Wirtz et al. (2018)'),('two classes, namely,','two classes:'),('Their system will allow','Their framework supports'),('and still keep employees on the job for cases that need them','while keeping employees for cases that need them'),('autonomous satisfaction tests','independent satisfaction tests'),('measure the performance of the tasks and the effort required by customers','measure task performance and customer effort'),('were found to differ depending on the frequency of visiting the bakery in a bakery study','varied with visit frequency in a bakery study'),('It has a remotely controlled robot, which restricts drawing conclusions','It used a remotely controlled robot, which limits conclusions')],
16:[('Where no discount is mentioned at F4 staff','Where a discount is missing at F4, staff'),('for the shopper not to have to start the process again','so the shopper need not restart')],
19:[('a paradox – between','a trade-off between'),('Purchase history as an aid to recommendations (Brazil\'s Nutri Choice, Carrefour 2021).',"Purchase history aids recommendations in Brazil's Nutri Choice (Carrefour, 2021)."),("the UAE assistant assistant's delicate dietary preferences if they are proposing to move to the UAE","customers' sensitive dietary preferences if used by the proposed UAE assistant"),('should be functioning properly at levels','should work at stages'),('Independent consent','Separate consent'),('consumers to opt-in for convenience without compromising on irrelevant information','customers to choose convenience without accepting unrelated data use'),('Short retention and limited access would limit exposure, but would also limit the amount of historical data which would undermine the personalisation.','Short retention and limited access would reduce exposure, but less historical data could weaken personalisation.')],
20:[('However, Huang','Huang'),('when no explicit instructions are given to discriminate','even without instructions to discriminate'),('If Carrefour chooses the profit margin route then it may prove harder to locate alternatives suitable and cheap products','If Carrefour prioritises profit margins, it may be harder to find suitable, cheaper products'),('Retailer should','The retailer should'),('Advertising should not rely on consumers being confused by advertising for the same content as non-advertising sources','Advertising should not rely on consumers mistaking sponsored advice for neutral information')],
21:[("Physical robotics doesn't impact just app users. ",''),('Some of the issues highlighted by Wirtz et al. (2018) involve','Wirtz et al. (2018) highlight'),('identifiable shoppers should be minimised and incidental images used and kept to a minimum','recording identifiable shoppers and retaining incidental images should be minimised'),('shall give way to humans and must','should give way to people and'),('Staffed assistance and Readable Instructions provide protection for customers who may lack digital confidence, language barriers or disabilities','Staffed assistance and readable instructions support customers with limited digital confidence, language barriers or disabilities'),("Equal access is expensive, self-service is free and it would be unfair to put the burden of such a business on those who can't afford it","Equal access costs money, but self-service savings should not depend on excluding those who cannot use it")],
22:[('take its shelf staff into consideration','involve shelf staff'),('pay for them to be trained','fund their training'),('If there is no stock then an unresolved alert','Without stock, an unresolved alert'),('and this does not absolve their duty to customers from using third party software','and third-party software does not remove their duty to customers'),('Alerts that are wrong can lead to greater','Incorrect alerts can increase'),('During this test of this risk, a limited pilot provides for service continuity','A limited pilot protects service continuity while testing this risk'),('The rank and workload should be audited weekly for managers','Rankings and workload should be audited weekly by managers')]
}
log=[]
for i,pairs in changes.items():
 p=ps[i]
 for old,new in pairs:
  s=text(p);assert s.count(old)==1,(i,old)
  start=s.index(old);end=start+len(old);pos=0
  nodes=p.xpath('.//w:t',namespaces=ns)
  for t in nodes:
   content=t.text or '';a=pos;b=pos+len(content);pos=b
   if b<=start or a>=end:continue
   left=max(0,start-a);right=min(len(content),end-a)
   t.text=content[:left]+(new if a<=start<b else '')+content[right:]
   t.set('{http://www.w3.org/XML/1998/namespace}space','preserve')
  assert text(p)==s.replace(old,new)
 log.append({'paragraph':i,'before':before[i],'after':text(p),'replacements':pairs})
# Body text was accidentally given Heading 1, creating bold text and page breaks.
for i in [10,11,19,20,21,22]:
 p=ps[i];pr=p.find('w:pPr',ns)
 if pr is not None:
  for n in list(pr):
   if n.tag in [f'{{{W}}}pStyle',f'{{{W}}}keepNext',f'{{{W}}}pageBreakBefore']:pr.remove(n)
 for n in p.xpath('.//w:rPr/w:b | .//w:rPr/w:bCs',namespaces=ns):n.getparent().remove(n)
# Keep each section heading together with its first paragraph.
for i in [4,7,12,18,23]:
 pr=ps[i].find('w:pPr',ns)
 if pr is None:pr=E.Element(f'{{{W}}}pPr');ps[i].insert(0,pr)
 if pr.find('w:keepNext',ns) is None:E.SubElement(pr,f'{{{W}}}keepNext')
after=[text(p) for p in ps];fi=next(i for i,t in enumerate(after) if t.startswith('Figure 1 Proposed'));main='\n'.join(after[:fi]);ft=(A/'Revision_2026-10-28/Source/blueprint_text.txt').read_text()
count=len(main.split())+len(ft.split());conservative=len(re.findall(r"\b\w+(?:['’]\w+)?\b",main+'\n'+ft))
print('WORDS',count,'CONSERVATIVE',conservative)
assert count<=2000 and conservative<=2000
assert before[29:]==after[29:]
parts['word/document.xml']=E.tostring(r,encoding='UTF-8',xml_declaration=True,standalone=True)
with ZipFile(out,'w',ZIP_DEFLATED) as z:
 for n,b in parts.items():z.writestr(n,b)
with ZipFile(src) as z:changed=[n for n in z.namelist() if z.read(n)!=parts[n]]
assert changed==['word/document.xml']
(R/'Source/edits.json').write_text(json.dumps(log,ensure_ascii=False,indent=2)+'\n')
(R/'Source/report_text.txt').write_text(main+'\n')
qa={'date':'2026-10-28','input_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'output_sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'word_count_including_blueprint_excluding_references':count,'conservative_word_count':conservative,'figure_and_references_preserved':True,'links_preserved':True,'changed_docx_parts':changed,'edited_paragraphs':list(changes),'render_review':'pending'}
(R/'Checks/REVISION.json').write_text(json.dumps(qa,indent=2)+'\n')
print(json.dumps(qa,indent=2))
