from pathlib import Path
from docx import Document
from docx.enum.section import WD_SECTION, WD_ORIENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Inches,Pt,RGBColor
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.opc.constants import RELATIONSHIP_TYPE as RT
import json,re,subprocess,sys
from PIL import Image
S=Path(__file__).resolve().parent
subprocess.run([sys.executable,str(S/'blueprint.py')],check=True)
D=S.parent
refs=[
 ('Badger Technologies. (2023, September 18). ','Badger Technologies and Stop & Shop stores upgrade Marty the Robot at 300+ locations to improve customer shopping experiences','. ','https://www.badger-technologies.com/news/press-releases/stop-and-shop-upgrade-marty-the-robot.html'),
 ('Bitner, M. J., Ostrom, A. L., & Morgan, F. N. (2008). Service blueprinting: A practical technique for service innovation. ','California Management Review, 50','(3), 66–94. ','https://doi.org/10.2307/41166446'),
 ('Carrefour Polska. (2022, October 25). ','Kerfuś ogłasza swoje pierwsze tournée i rusza w Polskę',' [Kerfuś announces its first tour across Poland]. ','https://serwiskorporacyjny.carrefour.pl/en/aktualnosci/O_Nas/Kerfus_Oglasza_Swoje_Pierwsze_Tournee_I_Rusza_W_Polske'),
 ('Carrefour UAE. (n.d.). ','How can I shop quickly and avoid queues at Carrefour?',' Retrieved November 1, 2026, from ','https://www.carrefouruae.com/mafuae/en/helpcenter/topics/212-browse-and-order?articleId=4221'),
 ('Huang, M.-H., & Rust, R. T. (2021). A strategic framework for artificial intelligence in marketing. ','Journal of the Academy of Marketing Science, 49','(1), 30–50. ','https://doi.org/10.1007/s11747-020-00749-9'),
 ('Majid Al Futtaim. (2022). ','Great moments for everyone, everyday: ESG report 2021','. ','https://www.majidalfuttaim.com/docs/default-source/reports/majid-al-futtaim-esg-report-2021-en.pdf?sfvrsn=ccf441f5_7'),
 ('Preda, I. (2022, November). ','The retail robot that solves in-store price and stock problem','. Adapta Robotics. ','https://www.adaptarobotics.com/blog/retail-robot-solves-in-store-problems/'),
 ('Tax, S. S., Brown, S. W., & Chandrashekaran, M. (1998). Customer evaluations of service complaint experiences: Implications for relationship marketing. ','Journal of Marketing, 62','(2), 60–76. ','https://doi.org/10.1177/002224299806200205'),
 ('thatguyDeni. (2023, March 31). ','Carrefour - Scan & Go 2020 commercial',' [Video]. Vimeo. ','https://vimeo.com/813563441'),
 ('Wirtz, J. (2023). ','Essentials of services marketing',' (4th ed.). Pearson.','')]
doc=Document();sect=doc.sections[0]
def size(sec,land=False):
 sec.orientation=WD_ORIENT.LANDSCAPE if land else WD_ORIENT.PORTRAIT
 sec.page_width=Inches(11.69 if land else 8.27);sec.page_height=Inches(8.27 if land else 11.69)
 sec.top_margin=Inches(.5 if land else .72);sec.bottom_margin=Inches(.5 if land else .69)
 sec.left_margin=sec.right_margin=Inches(.48 if land else .86);sec.footer_distance=Inches(.3)
size(sect)
norm=doc.styles['Normal'];norm.font.name='Calibri';norm.font.size=Pt(11.5);norm.font.color.rgb=RGBColor.from_string('1E3039')
norm.paragraph_format.line_spacing=1.10;norm.paragraph_format.space_after=Pt(6)
for st,sz in [('Title',25),('Heading 1',15),('Heading 2',12)]:
 v=doc.styles[st];v.font.name='Calibri';v.font.size=Pt(sz);v.font.color.rgb=RGBColor.from_string('123747');v.font.bold=True;v.paragraph_format.space_before=Pt(7);v.paragraph_format.space_after=Pt(5);v.paragraph_format.keep_with_next=True
 pr=v.element.get_or_add_pPr();border=pr.find(qn('w:pBdr'))
 if border is not None:pr.remove(border)
f=sect.footer.paragraphs[0];f.alignment=WD_ALIGN_PARAGRAPH.RIGHT
fr=f.add_run();fr.font.size=Pt(9);fld=OxmlElement('w:fldSimple');fld.set(qn('w:instr'),'PAGE');fr._r.addnext(fld)
doc.core_properties.author='Faiaz Dzhafarov, Muhammad Aun Abbas and Beky Sufyan';doc.core_properties.title='Grocery shopping at Carrefour UAE';doc.core_properties.subject='BUS225 Assessment 2';doc.core_properties.comments=''
for line in (S/'report.txt').read_text().splitlines():
 if not line:continue
 if line=='===':doc.add_page_break()
 elif line.startswith('# '):doc.add_paragraph(line[2:],'Title')
 elif line.startswith('~ '):
  p=doc.add_paragraph();p.paragraph_format.space_after=Pt(1);rr=p.add_run(line[2:]);rr.font.size=Pt(10);rr.font.color.rgb=RGBColor.from_string('47636D')
 elif line.startswith('## '):doc.add_paragraph(line[3:],'Heading 1')
 else:doc.add_paragraph(line)
sec=doc.add_section(WD_SECTION.NEW_PAGE);size(sec,True)
for i,(title,caption) in enumerate([
 ('Choosing a route and filling the basket','F1 marks an unavailable scanner, F2 an empty facing and F3 a duplicate scan. W marks a possible wait. Each support process feeds the task above it. Arrows across the line of visibility carry a request down and a response back.'),
 ('Checking the price, paying and resolving a charge','F4 marks a price mismatch and F5 a repeated complaint. For each stage the bottom row identifies the records each support process uses. Copper arrows carry price and payment evidence. Controls and standards are proposals. The customer routes follow Carrefour UAE (n.d.). Layout follows the class blueprint and Bitner et al. (2008).')]):
 if i:doc.add_page_break()
 p=doc.add_paragraph();p.paragraph_format.space_after=Pt(1);p.add_run('Figure 1'+(' (continued)' if i else '')).bold=True
 p=doc.add_paragraph();p.paragraph_format.space_after=Pt(3);p.add_run(title).italic=True
 p=doc.add_paragraph();p.alignment=WD_ALIGN_PARAGRAPH.CENTER;p.paragraph_format.space_after=Pt(0);p.paragraph_format.line_spacing=1.0
 sh=p.add_run().add_picture(str(S/f'panel_{i+1}.png'),width=Inches(10.52));sh._inline.docPr.set('descr',title+'. Stage-specific links connect each customer action to visible staff or equipment, backstage tasks, support teams and records.')
 p=doc.add_paragraph();p.paragraph_format.space_after=Pt(0);p.paragraph_format.line_spacing=1.0;r=p.add_run('Note. ');r.italic=True;r.font.size=Pt(9.5);p.add_run(caption).font.size=Pt(9.5)
sec=doc.add_section(WD_SECTION.NEW_PAGE);size(sec)
def link(p,url):
 h=OxmlElement('w:hyperlink');h.set(qn('r:id'),p.part.relate_to(url,RT.HYPERLINK,is_external=True));r=OxmlElement('w:r');pr=OxmlElement('w:rPr');c=OxmlElement('w:color');c.set(qn('w:val'),'205C71');pr.append(c);r.append(pr);t=OxmlElement('w:t');t.text=url;r.append(t);h.append(r);p._p.append(h)
p=doc.add_paragraph('References','Heading 1');p.alignment=WD_ALIGN_PARAGRAPH.CENTER
for i,(a,b,c,url) in enumerate(refs):
 if i==5:doc.add_page_break()
 p=doc.add_paragraph();pf=p.paragraph_format;pf.left_indent=Inches(.5);pf.first_line_indent=Inches(-.5);pf.space_after=Pt(0);pf.line_spacing=2.0;pf.keep_together=True
 p.add_run(a);p.add_run(b).italic=True;p.add_run(c)
 if url:link(p,url)
out=D/'BUS225_A2_Group9_Carrefour.docx';doc.save(out)
pp=[p.text for p in doc.paragraphs];main=' '.join(pp[:pp.index('References')])+' '+(S/'figure_words.txt').read_text()
counts={'words_whitespace':len(main.split()),'words_conservative_tokens':len(re.findall(r"\b[\w]+(?:[’'][\w]+)?\b",main)),'figure_text_extracted_from_drawing_labels':True,'references':len(refs)}
print(counts);assert max(counts['words_whitespace'],counts['words_conservative_tokens'])<=2000
(S/'counts.json').write_text(json.dumps(counts,indent=2)+'\n')
