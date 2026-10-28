from pathlib import Path
import json, math, re, html, subprocess
from reportlab.pdfgen import canvas
from reportlab.pdfbase.pdfmetrics import stringWidth
from docx import Document
from docx.shared import Inches, Pt, Cm, RGBColor
from docx.enum.section import WD_SECTION, WD_ORIENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.opc.constants import RELATIONSHIP_TYPE as RT
ROOT=Path(__file__).resolve().parents[1]; SRC=ROOT/'Source'
b=json.loads((SRC/'blueprint.json').read_text())
W,H=1080,640
c=canvas.Canvas(str(SRC/'service_blueprint_diagram.pdf'),pagesize=(W,H)); c.setTitle(b['title']);c.setAuthor('BUS225 Group 9')
svg=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">','<rect width="1080" height="640" fill="white"/>']
ink='#162434';blue='#215c79';light='#edf3f6';red='#9c312d';gray='#b9c4cb'
def line(x1,y1,x2,y2,color=blue,width=1,dash=False,arrow=False):
 c.setStrokeColor(color);c.setLineWidth(width);c.setDash([4,3] if dash else []);c.line(x1,H-y1,x2,H-y2)
 svg.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{width}"'+(' stroke-dasharray="4 3"' if dash else '')+'/>')
 if arrow:
  a=math.atan2(y2-y1,x2-x1);v=[(x2,y2),(x2-6*math.cos(a-.45),y2-6*math.sin(a-.45)),(x2-6*math.cos(a+.45),y2-6*math.sin(a+.45))]
  c.setFillColor(color);p=c.beginPath();p.moveTo(v[0][0],H-v[0][1]);p.lineTo(v[1][0],H-v[1][1]);p.lineTo(v[2][0],H-v[2][1]);p.close();c.drawPath(p,fill=1,stroke=0)
  svg.append('<polygon points="'+' '.join(f'{x},{y}' for x,y in v)+f'" fill="{color}"/>')
def rect(x,y,w,h,fill='white',stroke=gray):
 c.setFillColor(fill);c.setStrokeColor(stroke);c.setLineWidth(.7);c.setDash([]);c.rect(x,H-y-h,w,h,fill=1,stroke=1)
 svg.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" stroke="{stroke}" stroke-width="0.7"/>')
def text(x,y,s,size=14,bold=False,color=ink):
 f='Helvetica-Bold' if bold else 'Helvetica';c.setFillColor(color);c.setFont(f,size);c.drawString(x,H-y,s)
 svg.append(f'<text x="{x}" y="{y}" font-family="Arial, sans-serif" font-size="{size}" font-weight="{700 if bold else 400}" fill="{color}">{html.escape(s)}</text>')
def wrap(s,width,size=14,bold=False):
 f='Helvetica-Bold' if bold else 'Helvetica';lines=[];current=''
 for word in s.split():
  test=(current+' '+word).strip()
  if stringWidth(test,f,size)>width and current:lines.append(current);current=word
  else:current=test
 if current:lines.append(current)
 return lines
def block(x,y,s,w,size=14,bold=False,color=ink,leading=None):
 ls=wrap(s,w,size,bold);lead=leading or size*1.15
 for i,l in enumerate(ls):text(x,y+i*lead,l,size,bold,color)
 return len(ls)*lead
# All visual wording comes from blueprint.json.
text(8,20,b['subtitle'],16,True)
left=143;cw=154;gap=12;boxw=cw-gap
ys=[66,133,223,314,405];hs=[58,58,70,70,70]
for j,col in enumerate(b['columns']):
 x=left+j*cw;rect(x,33,boxw,27,blue,blue);text(x+8,52,col,14,True,'white')
for i,lane in enumerate(b['lanes']):
 block(8,ys[i]+20,lane['label'],125,14,True)
 for j,cell in enumerate(lane['cells']):
  x=left+j*cw;rect(x,ys[i],boxw,hs[i],light if i%2==0 else 'white')
  ls = (['1 Tally scans;', '3 Staff restock;', '4 Verify shelf', 'F2 W'] if (i,j)==(2,2) else ['2 Check stock;', 'assign task.', '5 Close alert;', 'update stock'] if (i,j)==(3,2) else wrap(cell,boxw-16,14))
  assert len(ls)*16<=hs[i]-6,(i,j,ls)
  for k,t in enumerate(ls):text(x+8,ys[i]+(hs[i]-len(ls)*16)/2+12+k*16,t,14,color=red if re.search(r'F[1-5]',cell) else ink)
  if i==1 and j<5:line(x+boxw,ys[i]+29,x+cw,ys[i]+29,arrow=True)
# Boundaries run through gutters; white label area reserved on left.
for yy,label in zip([207,298,389],b['boundaries']):
 line(left,yy,W-8,yy,gray,.8,True);block(5,yy-2,label,132,11.5,True,leading=12)
# Cross-lane handoffs in each column. No arrows overlay cell text.
for j in range(6):
 x=left+j*cw+boxw*.72
 for a,z in [(191,223),(293,314),(384,405)]:
  line(x,a,x,z,blue,1.25,arrow=True)
  line(x-9,z,x-9,a,blue,.8,arrow=True)
line(left+4*cw+boxw,440,left+5*cw,440,blue,1.25,arrow=True)
# Label selected handoffs in free strips above boundaries.
for j,s in zip([0,2,4,5],b['links']):
 x=left+j*cw
 text(x+1,485,s,11.3,False,blue)
# Return loop alongside stage 6, away from text.
x=left+5*cw+boxw+5
line(x,456,W-3,456,red,1.2);line(W-3,456,W-3,240,red,1.2);line(W-3,240,x,240,red,1.2,arrow=True)
text(8,509,b['controls_title'],15,True)
# Controls two columns, three rows with ample width.
for i,s in enumerate(b['controls']):
 x=8 if i<3 else 550;y=530+(i if i<3 else i-3)*19
 text(x,y,s,13.4)
text(550,568,b['stock_exception'],13.4)
block(8,589,b['legend'],W-16,13,leading=16)
block(8,621,b['standards'],W-16,13,leading=15)
c.save();svg.append('</svg>');(SRC/'service_blueprint.svg').write_text('\n'.join(svg))
subprocess.run(['/Users/king1/.cache/codex-runtimes/codex-primary-runtime/dependencies/bin/override/pdftoppm','-scale-to','3300','-singlefile','-png',str(SRC/'service_blueprint_diagram.pdf'),str(SRC/'service_blueprint')],check=True,stderr=subprocess.DEVNULL)
