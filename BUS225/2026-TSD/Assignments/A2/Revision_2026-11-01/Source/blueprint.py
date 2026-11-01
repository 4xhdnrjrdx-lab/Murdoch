from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import math, re
D=Path(__file__).resolve().parent
panels=[[('01  Enter',
   'Explain where scanning starts',
   'Enter to buy a few items',
   'Basket, entrance signs, scanner rack where offered',
   'Colleague explains optional Scan&Go route',
   'Prepare devices and assign entrance cover',
   'Charge scanners',
   'Roster entrance help',
   'Scanner status',
   'Staff roster',
   'F1',
   ''),
  ('02  Select items',
   'Check shelf before closing alert',
   'Pick snacks, drinks and household items',
   'Products, shelf tickets, Tally where deployed',
   'If a shelf is empty, refill it or explain shortage',
   'Check stockroom and assign refill task',
   'Locate stock',
   'Assign shelf alerts',
   'Stock record',
   'Shelf alert log',
   'F2',
   'W'),
  ('03  Choose lane',
   'Give a choice of checkout',
   'Choose Self Checkout over cashier line',
   'Cashier line, terminal, lane signs',
   'Show available terminals and staffed lane',
   'Allocate attendant cover across terminals',
   'Monitor terminal status',
   'Roster attendants',
   'Terminal status',
   'Staff roster',
   '',
   'W')],
 [('04  Scan and bag',
   'One recorded unit per item',
   'Retry unread barcode, then place item in bagging area',
   'English prompts, barcode reader, bagging area',
   'Display accepted item. Offer help if retries fail',
   'Check barcode match and preserve basket',
   'Maintain barcodes',
   'Update basket',
   'Item catalogue',
   'Basket record',
   'F3',
   'W'),
  ('05  Pay by card',
   'Confirm one successful charge',
   'Pay by bank card',
   'Payment screen, card terminal',
   'Terminal shows total and payment result',
   'Reconcile payment state before retry',
   'Retrieve basket',
   'Confirm payment',
   'Basket total',
   'Transaction log',
   '',
   ''),
  ('06  Query charge',
   'One case per disputed item',
   'If needed, query a charge',
   'Receipt line, help desk, case number',
   'Desk colleague explains adjustment and confirms outcome',
   'Review price evidence and authorise remedy',
   'Track dispute',
   'Validate price',
   'Case history',
   'Item and price record',
   'F4',
   'W')]]
rowlabels=['Timeline','Pilot standard','Customer actions','Physical evidence','Frontstage','Backstage','Support processes','Databases']
labels=[]; S=2; W=1450; H=860; rg='/System/Library/Fonts/Supplemental/Arial.ttf'; bd='/System/Library/Fonts/Supplemental/Arial Bold.ttf'
navy='#183549'; teal='#155965'; line='#71949B'; edge='#B9CBCF'; ink='#1C3440'; muted='#45616A'; rust='#9B4129'
def drawpanel(index,cols):
 im=Image.new('RGB',(W*S,H*S),'white');dr=ImageDraw.Draw(im); local=[]
 def txt(x,y,t,sz=18,bold=False,col=ink,anchor='lm',count=True):
  f=ImageFont.truetype(bd if bold else rg,sz*S);dr.text((x*S,y*S),t,font=f,fill=col,anchor=anchor)
  if count:local.append(t)
 def rect(a,b,c,e,fill,outline=None):
  dr.rectangle(tuple(v*S for v in (a,b,c,e)),fill=fill,outline=outline,width=S)
 def path(pts,col=line,wd=2):
  dr.line([(int(x*S),int(y*S)) for x,y in pts],fill=col,width=wd*S,joint='curve')
 def arrow(pts,col=teal):
  path(pts,col,2);(x0,y0),(x,y)=pts[-2:];a=math.atan2(y-y0,x-x0)
  dr.polygon([(x*S,y*S)]+[((x-8*math.cos(a+q))*S,(y-8*math.sin(a+q))*S) for q in [-.49,.49]],fill=col)
 def box(x,y,w,h,t,fill='#F5F8F8',sz=19,bold=False):
  rect(x,y,x+w,y+h,fill,edge);font=ImageFont.truetype(bd if bold else rg,sz*S)
  ls=[];current=''
  for wd in t.split():
   new=(current+' '+wd).strip()
   if dr.textlength(new,font=font)>(w-20)*S and current:ls.append(current);current=wd
   else:current=new
  ls.append(current);lh=sz+5;assert len(ls)*lh<=h+2,(t,ls,h)
  for j,st in enumerate(ls):txt(x+w/2,y+h/2+(j-(len(ls)-1)/2)*lh,st,sz,bold,anchor='mm',count=False)
  local.append(t)
 def boundary(y,t):
  for a in range(184,W-10,12):path([(a,y),(min(W-10,a+6),y)],'#9EADB2',1)
  txt(8,y,t,14,True,muted)
 for y,t in [(29,'Timeline'),(91,'Pilot standard'),(171,'Customer actions'),(264,'Physical evidence'),(370,'Frontstage'),(492,'Backstage'),(625,'Support processes'),(755,'Databases')]:txt(8,y,t,18,True)
 txt(8,395,'Visible to shopper',15,False,teal);txt(8,516,'Out of shopper’s view',15,False,muted)
 for y,t in [(325,'Line of interaction'),(432,'Line of visibility'),(554,'Line of internal interaction'),(706,'Internal IT interaction')]:boundary(y,t)
 for j,c in enumerate(cols):
  head,std,customer,evidence,front,back,s1,s2,d1,d2,fail,wait=c
  x=207+j*409;w=379;mid=x+w/2;left=x+91;right=x+w-91
  rect(x,6,x+w,52,navy);txt(x+12,29,head,23,True,'white')
  box(x,65,w,52,std,'#F8F8F4',17)
  box(x,139,w,68,customer,'#E4F2EE',20,True)
  if j<2:arrow([(x+w,173),(x+409,173)])
  box(x+13,234,w-26,63,evidence,'#FAFAF6',17)
  box(x,337,w,70,front,'#E3F1F2',18)
  box(x,456,w,75,back,'#ECEDF6',18)
  # Visible response reaches the customer around the evidence strip.
  arrow([(x+5,337),(x-11,337),(x-11,200),(x,200)])
  # The customer's request is handed down to the visible employee or device.
  arrow([(x+w,199),(x+w+10,199),(x+w+10,343),(x+w,343)])
  arrow([(left,407),(left,456)]);arrow([(right,456),(right,407)])
  for bx,t,db in [(x,s1,d1),(x+195,s2,d2)]:
   box(bx,587,184,76,t,'#F0F3F4',17);box(bx,721,184,70,db,'#F8FAFA',16)
   m=bx+92;arrow([(m,721),(m,663)])
   arrow([(m,587),(m,531)])
  if fail:txt(x+w-8,31,fail,17,True,'#FFDFAB',anchor='rm')
  if wait:
   cx=x+w-64;cy=29;path([(cx,cy-14),(cx-15,cy+12),(cx+15,cy+12),(cx,cy-14)],'#FFDFAB',1);txt(cx,cy+3,'W',13,True,'#FFDFAB',anchor='mm')
 if index:
  # Carry the successful payment to the service desk if the customer disputes it.
  arrow([(207+409+379,756),(207+818,756)],rust)
  arrow([(207+91,791),(207+91,806),(207+818+287,806),(207+818+287,791)],rust)
 else:
  txt(1220,810,'Terminal → stage 04',15,True,rust,anchor='mm')
 txt(8,830,('Continue to stage 04 on the next page.' if not index else 'For an unresolved price dispute, check the item recorded at stage 04 against the receipt.'),17,True,teal)
 out=D/('panel_'+str(index+1)+'.png');im.save(out,optimize=True);labels.extend(local)
if __name__=='__main__':
 for i,cols in enumerate(panels):drawpanel(i,cols)
 (D/'figure_words.txt').write_text('\n'.join(labels)+'\n')
