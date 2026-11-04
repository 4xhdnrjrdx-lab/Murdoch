"""Build a vector blueprint and insert it into the supplied report.

Run with the Codex bundled Python runtime. No source attachments are modified.
"""
from pathlib import Path
from copy import deepcopy
import json
import math
import re
import os
from xml.sax.saxutils import escape

from reportlab.graphics.shapes import Drawing, Rect, String, Line, Polygon
from reportlab.graphics import renderPDF, renderSVG
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.pdfbase.pdfmetrics import stringWidth
from docx import Document
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
import subprocess

HERE = Path(__file__).resolve().parent
OUT = HERE.parent
W, H = 1120, 790
INK, MUTED = '#22272B', '#4D5960'
EDGE, GREY, TEAL = '#D9D9D9', '#8C969B', '#286575'
BLUE = '#286575'
D = Drawing(W, H)
WORDS = []
TEXT_BOUNDS = []


def rect(x, y, w, h, fill, edge=EDGE):
    D.add(Rect(x, H-y-h, w, h, fillColor=HexColor(fill),
               strokeColor=HexColor(edge), strokeWidth=.7))


def line(points, col=GREY, width=1.1, dashed=False):
    for a, b in zip(points, points[1:]):
        obj = Line(a[0], H-a[1], b[0], H-b[1],
                   strokeColor=HexColor(col), strokeWidth=width)
        if dashed:
            obj.strokeDashArray = [4, 3]
        D.add(obj)


def tip(p, before, col):
    angle = math.atan2(p[1]-before[1], p[0]-before[0])
    pts = [p]
    for a in (-.46, .46):
        pts.append((p[0]-6*math.cos(angle+a), p[1]-6*math.sin(angle+a)))
    D.add(Polygon([v for x, y in pts for v in (x, H-y)],
                  fillColor=HexColor(col), strokeColor=None))


def arrow(points, col=GREY, both=False, width=1.1):
    line(points, col, width)
    tip(points[-1], points[-2], col)
    if both:
        tip(points[0], points[1], col)


def text(x, y, value, size=12, bold=False, col=INK, count=True):
    if count:
        WORDS.append(value)
    D.add(String(x, H-y-size*.80, value, fontName='Helvetica-Bold' if bold else 'Helvetica',
                 fontSize=size, fillColor=HexColor(col)))


def wrap(value, width, size, bold=False):
    font = 'Helvetica-Bold' if bold else 'Helvetica'
    result = []
    for part in value.split('\n'):
        current = ''
        for word in part.split():
            candidate = (current+' '+word).strip()
            if current and stringWidth(candidate, font, size) > width:
                result.append(current)
                current = word
            else:
                current = candidate
        result.append(current)
    return result


def block(x, y, w, h, value, fill='#F5F6F7', size=12, bold=False,
          col=INK, pad=9, heading=None):
    rect(x, y, w, h, fill)
    lines = wrap(value, w-pad*2, size, bold)
    lead = size*1.22
    head_height = 19 if heading else 0
    available = h-pad*2-head_height
    assert len(lines)*lead <= available+.5, (value, lines, available)
    ty = y+pad+head_height+(available-len(lines)*lead)/2
    if heading:
        assert stringWidth(heading, 'Helvetica-Bold', 11.5) <= w-pad*2, heading
        text(x+pad, y+pad, heading, 11.5, True)
    WORDS.append(value)
    for s in lines:
        text(x+pad, ty, s, size, bold, col, count=False)
        TEXT_BOUNDS.append((x+pad, ty, stringWidth(s, 'Helvetica-Bold' if bold else 'Helvetica', size), lead))
        ty += lead


def row_label(y, value):
    for j, part in enumerate(value.split('\n')):
        text(22, y+j*14, part, 11.4, True, MUTED)


def boundary(y, label):
    line([(148, y), (1098, y)], '#9DA6AA', .9, True)
    for j, part in enumerate(label.split('\n')):
        text(22, y-7+j*11, part, 9.3, False, MUTED)


stages = [
    dict(title='01 ARRIVE', evidence='Entrance signs; scanners or\napp; checkout lanes.',
         customer='Choose cashier, Scan&Go\nor self-checkout.',
         front='Explain options; help\nstart Scan&Go.',
         back='Check device readiness;\nassign store assistance.',
         support='Device support;\nstaff rota and instructions.',
         dbtitle='D1 Devices and staffing', db='Device ID; status;\nshift and help cover.',
         fail='F1 Cannot start scanning',
         recovery='P Clear instructions;\nstaffed checkout available.'),
    dict(title='02 FIND AND SELECT', evidence='Products; shelf labels;\nTally where deployed.',
         customer='Find and choose products;\nask about missing stock.',
         front='Tally checks shelves where\nused; staff answer stock queries.',
         back='Review alert; check stock;\nassign shelf replenishment.',
         support='Inventory control;\nalert queue and replenishment.',
         dbtitle='D2 Products and stock', db='SKU/barcode; shelf quantity;\nalert and refill status.',
         fail='F2 Empty shelf',
         recovery='P Named alert owner;\nconfirm refill or explain shortage.'),
    dict(title='03 SCAN AND REVIEW', evidence='Barcode; basket display;\nscanner or checkout terminal.',
         customer='Scan&Go: scan in aisles.\nSelf-checkout: scan at till.\nCashier: hand over basket.',
         front='Terminal shows scanned item;\ncashier scans; attendant helps.',
         back='Verify barcode, price and\npromotions; correct item.',
         support='Product catalogue;\nprice updates and basket system.',
         dbtitle='D3 Prices and basket', db='Item; quantity; price;\npromotion; basket total.',
         fail='F3 Scan or price error',
         recovery='P Check item; recover basket\nwhere technically possible.'),
    dict(title='04 PAY AND LEAVE', evidence='Total; payment screen;\nreceipt; exit signs.',
         customer='Check total; pay;\ncollect receipt and leave.',
         front='Confirm payment; help with\ndeclines or a stopped terminal.',
         back='Check payment status;\nauthorise exceptions.',
         support='Payment gateway;\nterminal and transaction support.',
         dbtitle='D4 Sales and payments', db='Transaction ID; payment status;\nitemised receipt.',
         fail='F4 Delay or payment failure',
         recovery='P Allocate attendant;\ncheck status before retry.'),
    dict(title='05 AFTERCARE', evidence='Receipt; service desk;\ncase reference.',
         customer='If needed, query a charge\nor request a return.',
         front='Hear complaint; explain\ncorrection or return.',
         back='Review receipt and item;\nauthorise remedy or escalate.',
         support='Receipt lookup;\nreturns policy and case handling.',
         dbtitle='D5 Returns and complaints', db='Case ID; receipt reference;\nreason; remedy and outcome.',
         fail='F5 Repeated explanation',
         recovery='P Transfer receipt and case;\nassign one case owner.'),
]

text(22, 16, 'BUS225  /  SERVICES MARKETING  /  GROUP 9', 10, False)
text(22, 36, 'Figure 1 Carrefour UAE service blueprint', 21, True, '#000000')
text(22, 64, 'Physical store journey  |  F = potential failure  |  P = proposed improvement', 11)
start, gap, cw = 148, 10, 182
for i, s in enumerate(stages):
    x = start+i*(cw+gap)
    rect(x, 88, cw, 34, '#292E32', '#292E32')
    text(x+9, 99, s['title'], 12, True, '#FFFFFF')
    block(x, 132, cw, 47, s['evidence'], size=11.7, pad=7)
    block(x, 192, cw, 58, s['customer'], size=11.9, pad=7)
    if i < 4:
        arrow([(x+cw, 221), (x+cw+gap, 221)])
    block(x, 279, cw, 68, s['front'], size=11.9, pad=8)
    block(x, 376, cw, 58, s['back'], size=11.9, pad=7)
    block(x, 463, cw, 59, s['support'], size=11.7, pad=7)
    # Requests and responses cross the line separating visible and hidden work.
    arrow([(x+cw/2, 250), (x+cw/2, 279)], both=True)
    arrow([(x+cw/2, 347), (x+cw/2, 376)], both=True)
    arrow([(x+cw/2, 434), (x+cw/2, 463)], both=True)
    block(x, 577, cw, 73, s['db'], '#EAF1F4', 11.6, pad=7, heading=s['dbtitle'])
    # The records directly support the service process in the same column.
    arrow([(x+cw/2-35, 577), (x+cw/2-35, 522)], BLUE, both=True, width=1.25)
    block(x, 666, cw, 38, s['fail'], '#FAEEE7', 11.7, True, '#854830', pad=7)
    arrow([(x+cw/2, 704), (x+cw/2, 714)], '#A36A53')
    block(x, 714, cw, 48, s['recovery'], '#EDF3EF', 11.5, pad=6)

# Data shared between stages, in addition to each column's direct record link.
# Products supply barcode details to scanning. Basket totals feed payment.
# Payment receipts feed aftercare. These are required design links, not a claim
# about Carrefour's internal software architecture.
for source, target, track in [(1, 2, 542), (2, 3, 552), (3, 4, 562)]:
    sx = start+source*(cw+gap)+cw/2+34
    tx = start+target*(cw+gap)+cw/2+34
    arrow([(sx, 577), (sx, track), (tx, track), (tx, 522)], BLUE, width=1.25)

row_label(145, 'PHYSICAL\nEVIDENCE')
row_label(204, 'CUSTOMER\nACTIONS')
row_label(295, 'FRONTSTAGE\nStaff and interfaces')
row_label(390, 'BACKSTAGE\nStaff and operations')
row_label(478, 'SUPPORT\nPROCESSES')
row_label(594, 'IT SYSTEMS\nAND DATABASES')
row_label(676, 'FAILURE\nPOINTS')
row_label(725, 'PREVENTION\nAND RECOVERY')
boundary(265, 'Line of external\ninteraction')
boundary(362, 'Line of visibility')
boundary(448, 'Line of internal\ninteraction')
boundary(536, 'Line of internal\nIT interaction')

# One concise note identifies the meaning of the links and the design's limits.
# Notes are outside the main frame to avoid confusing them with database data.
note1 = 'Grey arrows: service handovers. Blue arrows: data flows. Scan&Go repeats stages 2-3 while shopping.'
note2 = 'Internal activities and data links show a proposed service design. Tally availability varies by store.'
note3 = 'Sources: Bitner et al. (2008); Carrefour UAE (n.d.); Majid Al Futtaim (2022).'
# Notes are placed on a separate strip by extending the artboard slightly.
for y, note in [(774, note1), (789, note2), (804, note3)]:
    text(22, y, note, 10.4)
H_OUT = 822
# Increase the canvas without changing the drawing's top-based positions.
D.translate(0, H_OUT-H)
D.height = H_OUT

svg = OUT/'Carrefour_Service_Blueprint.svg'
pdf = OUT/'Carrefour_Service_Blueprint.pdf'
png = OUT/'Carrefour_Service_Blueprint.png'
renderSVG.drawToFile(D, str(svg))
# An A4 landscape PDF keeps the diagram easy to print and share.
page_w, page_h = 841.8898, 595.2756
c = canvas.Canvas(str(pdf), pagesize=(page_w, page_h))
c.setTitle('Carrefour UAE service blueprint')
c.setAuthor('Group 9')
scale = min(page_w/W, page_h/H_OUT)
c.translate((page_w-W*scale)/2, (page_h-H_OUT*scale)/2)
c.scale(scale, scale)
renderPDF.draw(D, c, 0, 0)
c.showPage()
c.save()
font_conf = Path('/private/tmp/bus225-blueprint-fonts.conf')
font_cache = Path('/private/tmp/bus225-blueprint-font-cache')
font_cache.mkdir(exist_ok=True)
font_conf.write_text('<?xml version="1.0"?><!DOCTYPE fontconfig SYSTEM "fonts.dtd">'
    '<fontconfig><dir>/System/Library/Fonts</dir><dir>/Library/Fonts</dir>'
    '<cachedir>'+str(font_cache)+'</cachedir></fontconfig>')
env = dict(os.environ, FONTCONFIG_FILE=str(font_conf), XDG_CACHE_HOME=str(font_cache))
result = subprocess.run(['pdftoppm', '-r', '288', '-png', '-singlefile', str(pdf),
    str(png.with_suffix(''))], env=env, capture_output=True, text=True)
if result.returncode:
    raise RuntimeError(result.stderr[-1500:])
(HERE/'blueprint_text.txt').write_text('\n'.join(WORDS)+'\n')
(HERE/'blueprint_data.json').write_text(json.dumps(stages, indent=2)+'\n')

# Preserve the report and references; replace both old blueprint panels.
src = HERE/'Muhammad_Received_2026-11-04.docx'
doc = Document(src)
body = doc._element.body
children = list(body)
first = next(i for i, el in enumerate(children)
             if ''.join(el.itertext()).startswith('Service blueprint Entering'))
last = next(i for i, el in enumerate(children)
            if ''.join(el.itertext()).startswith('References'))
end_section = deepcopy(children[last-1])
assert end_section.find('.//'+qn('w:sectPr')) is not None
for el in children[first:last]:
    body.remove(el)
anchor = children[last]
# Add a picture paragraph with a small exact line height and no empty heading.
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.paragraph_format.space_before = Pt(0)
p.paragraph_format.space_after = Pt(0)
p.paragraph_format.line_spacing = 1
pic = p.add_run().add_picture(str(png), width=Inches(10))
pic._inline.docPr.set('descr', 'Carrefour physical store service blueprint with five stages, '
    'customer actions, frontstage, backstage, support processes, separate IT records, '
    'linked data flows, failures F1 to F5 and proposed recovery controls.')
anchor.addprevious(p._p)
anchor.addprevious(end_section)
# Section 0 remains the supplied portrait report; section 1 is the landscape
# blueprint; section 2 returns to the original portrait references.
assert len(doc.sections) == 3
sec = doc.sections[1]
sec.top_margin = Inches(.42)
sec.bottom_margin = Inches(.42)
# Remove generator comments rather than claiming unaided authorship.
doc.core_properties.title = 'Robotics and the Carrefour UAE store journey'
doc.core_properties.subject = 'BUS225 Assessment 2 Group 9'
doc.core_properties.comments = ''
doc.core_properties.last_modified_by = ''
out_docx = OUT/'BUS225_A2_Group9_Carrefour_Updated.docx'
doc.save(out_docx)

source_doc = Document(src)
source_text = [p.text for p in source_doc.paragraphs]
new_text = [p.text for p in doc.paragraphs]
report_start = source_text.index('1 Scope and service context')
ref_start = source_text.index('References')
report_original = source_text[:27]
assert new_text[:27] == report_original, 'Report paragraphs changed'
assert new_text[new_text.index('References'):] == source_text[ref_start:], 'References changed'
report = '\n'.join(t for t in report_original if t)
combined = report+'\n'+'\n'.join(WORDS)
counts = {
    'report_words_whitespace': len(report.split()),
    'blueprint_words_whitespace': len(' '.join(WORDS).split()),
    'combined_words_whitespace': len(combined.split()),
    'combined_words_regex': len(re.findall(r"\b[\w]+(?:[’'-][\w]+)*\b", combined)),
    'references_excluded': True,
    'report_and_references_preserved': True,
    'diagram_cell_overflow_assertions': 'pass',
    'expected_pages': 5,
}
assert max(counts['combined_words_whitespace'], counts['combined_words_regex']) <= 2000, counts
(HERE/'counts.json').write_text(json.dumps(counts, indent=2)+'\n')
print(json.dumps(counts, indent=2))
