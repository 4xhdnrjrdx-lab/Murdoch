#!/usr/bin/env python3
# Build BUS363 A2 Individual Project Plan slide deck (Murdoch LMS App v2.0).
import os, sys
try:
    from pptx import Presentation
    from pptx.util import Inches, Pt, Emu
    from pptx.dml.color import RGBColor
    from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    os.system(f"{sys.executable} -m pip install --quiet python-pptx pillow")
    from pptx import Presentation
    from pptx.util import Inches, Pt, Emu
    from pptx.dml.color import RGBColor
    from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
    from PIL import Image, ImageDraw, ImageFont

OUT = "/Users/king1/Documents/Murdoch/BUS363"
ASSETS = os.path.join(OUT, "_assets")
os.makedirs(ASSETS, exist_ok=True)

# ---- Murdoch palette ----
RED   = (200, 16, 46)      # Murdoch red
DRED  = (122, 0, 25)
DARK  = (38, 38, 38)
GREY  = (90, 90, 90)
LGREY = (232, 232, 232)
WHITE = (255, 255, 255)
GREEN = (76, 160, 80)
AMBER = (240, 173, 60)
REDX  = (214, 64, 64)

def font(sz, bold=False):
    paths = [
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
    ]
    for p in paths:
        try: return ImageFont.truetype(p, sz)
        except: pass
    return ImageFont.load_default()

def tsize(d, t, f):
    b = d.textbbox((0,0), t, font=f); return b[2]-b[0], b[3]-b[1]

# ================= Pillow diagrams =================
def diag_lifecycle():
    W,H = 1800,360; im=Image.new("RGB",(W,H),WHITE); d=ImageDraw.Draw(im)
    phases=[("1. Initiation","M1"),("2. Discovery & Design","M1–M2"),
            ("3. Iterative Development","M2–M5"),("4. UAT","M4–M5"),
            ("5. Deployment & Go-live","M5–M6"),("6. Hypercare & Close","M6")]
    n=len(phases); gap=14; cw=(W-(n-1)*gap-40)//n; x=20; y=90; h=150; tip=34
    f1=font(30,True); f2=font(26)
    for i,(name,mo) in enumerate(phases):
        col = RED if i%2==0 else DRED
        x0=x; x1=x+cw
        pts=[(x0,y),(x1-tip,y),(x1,y+h//2),(x1-tip,y+h),(x0,y+h),(x0+tip,y+h//2)]
        if i==0: pts=[(x0,y),(x1-tip,y),(x1,y+h//2),(x1-tip,y+h),(x0,y+h)]
        d.polygon(pts,fill=col)
        # wrap name
        words=name.split(); lines=[]; cur=""
        for w in words:
            t=(cur+" "+w).strip()
            if tsize(d,t,f1)[0] < cw-tip-20: cur=t
            else: lines.append(cur); cur=w
        lines.append(cur)
        ty=y+h//2-len(lines)*20-12
        for ln in lines:
            tw,_=tsize(d,ln,f1); d.text((x0+(cw-tip)//2-tw//2+8,ty),ln,fill=WHITE,font=f1); ty+=40
        mw,_=tsize(d,mo,f2); d.text((x0+(cw-tip)//2-mw//2+8,y+h+16),mo,fill=GREY,font=f2)
        x+=cw+gap
    p=os.path.join(ASSETS,"lifecycle.png"); im.save(p); return p

def diag_org():
    W,H=1800,1000; im=Image.new("RGB",(W,H),WHITE); d=ImageDraw.Draw(im)
    ft=font(30,True); fb=font(24)
    def box(cx,cy,w,h,title,lines,fill=RED,tcol=WHITE):
        x0,y0=cx-w//2,cy-h//2; d.rounded_rectangle([x0,y0,x0+w,y0+h],radius=14,fill=fill)
        tw,_=tsize(d,title,ft); d.text((cx-tw//2,y0+14),title,fill=tcol,font=ft)
        ty=y0+58
        for ln in lines:
            tw,_=tsize(d,ln,fb); d.text((cx-tw//2,ty),ln,fill=tcol,font=fb); ty+=32
        return (cx,cy,w,h)
    def line(a,b): d.line([a,b],fill=GREY,width=3)
    # Board top
    board=box(900,90,560,120,"Project Board",["Murdoch IT Sponsor (Director)","+ Vendor Director"],fill=DRED)
    # Oversight (side)
    over=box(300,300,440,120,"Oversight / Assurance",["Delivery assurance","Technical assurance"],fill=GREY)
    # PM center
    pm=box(900,330,560,120,"Project Management",["Vendor PM","Client Product Owner"],fill=RED)
    line((900,150),(900,270))
    line((520,300),(620,330))
    # three delivery groups
    g1=box(380,640,460,210,"Design & Analysis",["BA","Solution Architect","UX Designer","Infrastructure","Test Lead"],fill=(70,90,120))
    g2=box(900,640,460,210,"Technical",["Tech Lead","Developers (x2)","QA / Testers"],fill=(70,90,120))
    g3=box(1420,640,460,210,"Adoption & Change",["BA","Training"],fill=(70,90,120))
    line((900,390),(900,470)); line((900,470),(380,470)); line((900,470),(1420,470))
    line((380,470),(380,535)); line((900,470),(900,535)); line((1420,470),(1420,535))
    p=os.path.join(ASSETS,"org.png"); im.save(p); return p

def diag_gantt():
    W,H=1800,820; im=Image.new("RGB",(W,H),WHITE); d=ImageDraw.Draw(im)
    fh=font(26,True); fr=font(24); fm=font(24,True)
    rows=[("Initiation",1,1),("Discovery & Design",1,2),("Iterative Development (Sprints 1–8)",2,5),
          ("UAT",4,5),("Infrastructure & Deployment",5,6),("Data & Migration",3,5),
          ("Training & Adoption",5,6),("Hypercare & Support",6,6)]
    left=560; top=90; mcol=190; rowh=72; months=6
    # header
    for m in range(months):
        x=left+m*mcol; d.rectangle([x,top-50,x+mcol-6,top-8],fill=RED)
        t=f"Month {m+1}"; tw,_=tsize(d,t,fh); d.text((x+(mcol-6)//2-tw//2,top-46),t,fill=WHITE,font=fh)
    for i,(name,s,e) in enumerate(rows):
        y=top+i*rowh
        if i%2==0: d.rectangle([0,y,left+months*mcol,y+rowh-6],fill=(247,247,247))
        # wrap label
        words=name.split(); lines=[]; cur=""
        for w in words:
            t=(cur+" "+w).strip()
            if tsize(d,t,fr)[0]<left-20: cur=t
            else: lines.append(cur); cur=w
        lines.append(cur); ty=y+rowh//2-len(lines)*15-6
        for ln in lines: d.text((14,ty),ln,fill=DARK,font=fr); ty+=30
        x0=left+(s-1)*mcol+8; x1=left+e*mcol-12
        d.rounded_rectangle([x0,y+16,x1,y+rowh-22],radius=10,fill=RED if i!=2 else DRED)
    # grid lines
    for m in range(months+1):
        x=left+m*mcol; d.line([x,top-8,x,top+len(rows)*rowh-6],fill=LGREY,width=2)
    # milestones row (name, month, fraction-in-month, label-level for vertical stagger)
    my=top+len(rows)*rowh+18
    ms=[("Kick-off",1,0.5,0),("Design sign-off",2,0.5,0),("Feature complete",5,0.55,0),
        ("UAT sign-off",5,0.92,1),("Go-live",6,0.35,0),("Close",6,0.78,1)]
    fm2=font(22,True)
    for name,m,frac,lvl in ms:
        x=int(left+(m-1)*mcol+frac*mcol)
        d.polygon([(x,my),(x+15,my+15),(x,my+30),(x-15,my+15)],fill=DRED)
        tw,_=tsize(d,name,fm2); d.text((x-tw//2,my+34+lvl*36),name,fill=DRED,font=fm2)
    p=os.path.join(ASSETS,"gantt.png"); im.save(p); return p

def diag_riskmatrix():
    W,H=900,820; im=Image.new("RGB",(W,H),WHITE); d=ImageDraw.Draw(im)
    fa=font(24,True); fc=font(28,True)
    n=5; cell=130; ox=170; oy=70
    def color(l,c):
        s=l*c
        if s>=15: return (224,108,108)
        if s>=8: return (244,200,120)
        return (150,200,150)
    for li in range(n):       # likelihood rows (bottom=1)
        for ci in range(n):   # consequence cols (left=1)
            l=n-li; c=ci+1
            x0=ox+ci*cell; y0=oy+li*cell
            d.rectangle([x0,y0,x0+cell-4,y0+cell-4],fill=color(l,c))
    # axis labels
    d.text((ox,oy-46),"Consequence  →",fill=DARK,font=fa)
    # vertical likelihood label
    lab=Image.new("RGB",(260,40),WHITE); ld=ImageDraw.Draw(lab); ld.text((0,0),"Likelihood  →",fill=DARK,font=fa)
    lab=lab.rotate(90,expand=True); im.paste(lab,(20,oy+60))
    for i in range(n):
        d.text((ox+i*cell+cell//2-8,oy+n*cell+8),str(i+1),fill=GREY,font=fa)   # consequence 1..5
        d.text((ox-40,oy+i*cell+cell//2-12),str(n-i),fill=GREY,font=fa)        # likelihood 5..1
    # plot risks  (likelihood, consequence)
    risks={"R1":(4,5),"R2":(3,4),"R3":(3,5),"R4":(3,3),"R5":(3,3),"R6":(2,3)}
    placed={}
    for r,(l,c) in risks.items():
        cx=ox+(c-1)*cell+cell//2; cy=oy+(n-l)*cell+cell//2
        key=(l,c); off=placed.get(key,0); placed[key]=off+1; cx+=off*42-20
        d.ellipse([cx-26,cy-26,cx+26,cy+26],fill=DRED,outline=WHITE,width=3)
        tw,_=tsize(d,r,fc); d.text((cx-tw//2,cy-16),r,fill=WHITE,font=fc)
    p=os.path.join(ASSETS,"riskmatrix.png"); im.save(p); return p

def diag_mendelow():
    W,H=1500,860; im=Image.new("RGB",(W,H),WHITE); d=ImageDraw.Draw(im)
    ft=font(34,True); fb=font(26); fsub=font(22); fa=font(26,True)
    ox,oy,sz=120,70,680
    quads=[((ox,oy),(150,150,170),"Keep Satisfied","High power · Low interest",["University Executive","Finance"]),
           ((ox+sz//2,oy),(200,16,46),"Manage Closely","High power · High interest",["Project Board / Sponsor","Product Owner"]),
           ((ox,oy+sz//2),(170,170,170),"Monitor","Low power · Low interest",["Other departments"]),
           ((ox+sz//2,oy+sz//2),(70,90,120),"Keep Informed","Low power · High interest",["Students (end users)","Lecturers","Help Desk","Library"])]
    for (px,py),col,title,sub,names in quads:
        d.rectangle([px,py,px+sz//2-6,py+sz//2-6],fill=col)
        d.text((px+20,py+18),title,fill=WHITE,font=ft)
        d.text((px+20,py+60),sub,fill=WHITE,font=fsub)
        ty=py+106
        for nm in names: d.text((px+20,ty),"• "+nm,fill=WHITE,font=fb); ty+=38
    # axes labels
    d.text((ox+sz//2-40,oy+sz+14),"Interest  →",fill=DARK,font=fa)
    lab=Image.new("RGB",(220,40),WHITE); ld=ImageDraw.Draw(lab); ld.text((0,0),"Power  →",fill=DARK,font=fa)
    lab=lab.rotate(90,expand=True); im.paste(lab,(ox-70,oy+sz//2-40))
    p=os.path.join(ASSETS,"mendelow.png"); im.save(p); return p

# ================= PPTX build =================
prs=Presentation(); prs.slide_width=Inches(13.333); prs.slide_height=Inches(7.5)
BLANK=prs.slide_layouts[6]
SW,SH=prs.slide_width,prs.slide_height
def C(rgb): return RGBColor(*rgb)

def slide():
    return prs.slides.add_slide(BLANK)

def title_bar(s, text, num=None):
    bar=s.shapes.add_shape(1, 0, 0, SW, Inches(1.0))
    bar.fill.solid(); bar.fill.fore_color.rgb=C(RED); bar.line.fill.background()
    tb=s.shapes.add_textbox(Inches(0.5), Inches(0.12), SW-Inches(1.0), Inches(0.78))
    tf=tb.text_frame; tf.word_wrap=True; p=tf.paragraphs[0]
    r=p.add_run(); r.text=text; r.font.size=Pt(30); r.font.bold=True; r.font.color.rgb=C(WHITE); r.font.name="Arial"
    p.alignment=PP_ALIGN.LEFT; tf.vertical_anchor=MSO_ANCHOR.MIDDLE

def notes(s, text):
    s.notes_slide.notes_text_frame.text=text

def bullets(s, items, left, top, width, height, size=18, gap=6):
    tb=s.shapes.add_textbox(left, top, width, height); tf=tb.text_frame; tf.word_wrap=True
    for i,(txt,lvl) in enumerate(items):
        p=tf.paragraphs[0] if i==0 else tf.add_paragraph()
        p.level=lvl; r=p.add_run(); r.text=("• " if lvl==0 else "– ")+txt
        r.font.size=Pt(size- (2 if lvl else 0)); r.font.name="Arial"; r.font.color.rgb=C(DARK if lvl==0 else GREY)
        p.space_after=Pt(gap)
    return tb

def heading(s, text, left, top, width, color=DRED, size=18):
    tb=s.shapes.add_textbox(left, top, width, Inches(0.4)); p=tb.text_frame.paragraphs[0]
    r=p.add_run(); r.text=text; r.font.bold=True; r.font.size=Pt(size); r.font.color.rgb=C(color); r.font.name="Arial"
    return tb

def table(s, data, left, top, width, height, header=True, col_w=None, fs=13):
    rows=len(data); cols=len(data[0])
    gt=s.shapes.add_table(rows, cols, left, top, width, height).table
    if col_w:
        for ci,w in enumerate(col_w): gt.columns[ci].width=w
    for ri,row in enumerate(data):
        for ci,val in enumerate(row):
            cell=gt.cell(ri,ci); cell.margin_left=Inches(0.06); cell.margin_right=Inches(0.06)
            cell.margin_top=Inches(0.02); cell.margin_bottom=Inches(0.02)
            tf=cell.text_frame; tf.word_wrap=True; p=tf.paragraphs[0]; r=p.add_run(); r.text=str(val)
            r.font.size=Pt(fs); r.font.name="Arial"
            if header and ri==0:
                cell.fill.solid(); cell.fill.fore_color.rgb=C(RED); r.font.bold=True; r.font.color.rgb=C(WHITE)
            else:
                cell.fill.solid(); cell.fill.fore_color.rgb=C(WHITE if ri%2 else (245,245,245)); r.font.color.rgb=C(DARK)
    return gt

def pic(s, path, left, top, width=None, height=None):
    return s.shapes.add_picture(path, left, top, width=width, height=height)

# ---- Slide 1: Title
s=slide()
bg=s.shapes.add_shape(1,0,0,SW,SH); bg.fill.solid(); bg.fill.fore_color.rgb=C(DRED); bg.line.fill.background()
band=s.shapes.add_shape(1,0,Inches(2.6),SW,Inches(2.2)); band.fill.solid(); band.fill.fore_color.rgb=C(RED); band.line.fill.background()
tb=s.shapes.add_textbox(Inches(0.8),Inches(2.7),SW-Inches(1.6),Inches(2.0)); tf=tb.text_frame; tf.word_wrap=True
p=tf.paragraphs[0]; r=p.add_run(); r.text="Murdoch Student LMS App v2.0"; r.font.size=Pt(44); r.font.bold=True; r.font.color.rgb=C(WHITE); r.font.name="Arial"
p2=tf.add_paragraph(); r=p2.add_run(); r.text="Individual Project Plan"; r.font.size=Pt(30); r.font.color.rgb=C(WHITE); r.font.name="Arial"
tb2=s.shapes.add_textbox(Inches(0.8),Inches(5.2),SW-Inches(1.6),Inches(1.8)); tf2=tb2.text_frame; tf2.word_wrap=True
for i,line in enumerate(["Faiaz Dzhafarov  ·  Student ID 35553299",
                         "BUS363 Scaling Agile Projects  ·  Assessment 2",
                         "Workshop: Thursday 2:00–4:00 pm (Rm 106)  ·  Tutor: Dr Leena Wanganoo",
                         "Unit Coordinator: Vesna Sampson  ·  TMD 2026"]):
    p=tf2.paragraphs[0] if i==0 else tf2.add_paragraph(); r=p.add_run(); r.text=line
    r.font.size=Pt(16); r.font.color.rgb=C(WHITE); r.font.name="Arial"
notes(s,"Good morning. I'm presenting my project plan for version 2.0 of the Murdoch Student LMS App. It's a fixed-price job: half a million dollars, six months. I'll cover the objectives and scope, how I'd run the project, the timeline and billing, the main risks, and how I'd keep it under control commercially.")

# ---- Slide 2: Background & Objectives
s=slide(); title_bar(s,"Background & Objectives")
bullets(s,[
 ("Context: IT delivery firm engaged to build LMS App v2.0, fixed price A$500k, 6 months, requirements signed off.",0),
 ("Vision: a fast, mobile-first app, one place for timetable, grades, unit materials, notifications and submissions.",0),
 ("Goals (SMART):",0),
 ("Ship v2.0 in 6 months within A$500k budget",1),
 ("≥99.5% crash-free sessions; SSO with myMurdoch",1),
 ("≥80% active-student adoption within 3 months of launch",1),
 ("Key deliverables: cross-platform app (iOS/Android); system integrations; Systems Manual; 3-month hypercare.",0),
 ("Assumptions: requirements frozen at kickoff; Murdoch provides API access + test data; one client Product Owner available.",0),
],Inches(0.6),Inches(1.25),SW-Inches(1.2),Inches(5.8),size=19,gap=8)
notes(s,"Two things matter here. The price and scope are fixed, so the whole plan exists to protect time and quality. And the goals are written so I can actually measure them later. I've put the assumptions up front too, because if Murdoch can't give us API access early, a lot of this plan shifts.")

# ---- Slide 3: Scope
s=slide(); title_bar(s,"Scope")
heading(s,"In scope",Inches(0.6),Inches(1.2),Inches(6))
bullets(s,[("Cross-platform app (iOS / Android)",0),("SSO; timetable, grades, materials (offline), push notifications, submissions",0),
 ("Integration with existing Murdoch systems",0),("UAT, deployment, 3-month post-go-live support",0)],
 Inches(0.6),Inches(1.6),Inches(6.1),Inches(2.6),size=16)
heading(s,"Out of scope",Inches(6.9),Inches(1.2),Inches(6))
bullets(s,[("Changes to Moodle core / back-end",0),("New academic content",0),
 ("Staff training beyond admin handover",0),("Hardware procurement",0)],
 Inches(6.9),Inches(1.6),Inches(5.8),Inches(2.6),size=16)
heading(s,"Constraints & baseline",Inches(0.6),Inches(4.4),Inches(11))
bullets(s,[("Fixed price A$500k & fixed scope → schedule and quality are the managed levers (triple constraint).",0),
 ("6-month hard deadline; university data-privacy & security policy.",0),
 ("Scope baseline = scope statement + WBS + schedule (100% rule: all work captured, nothing extra).",0)],
 Inches(0.6),Inches(4.8),SW-Inches(1.2),Inches(2.2),size=16)
notes(s,"Cost and scope are locked by the contract. That leaves schedule and quality as the levers I actually manage, and I run those through change control. Anything a stakeholder asks for later gets checked against the scope baseline before it goes near the backlog.")

# ---- Slide 4: Approach & Governance
s=slide(); title_bar(s,"Project Approach & Governance")
bullets(s,[("Hybrid approach:",0),
 ("Predictive outer shell: stage gates, fixed milestones, milestone-based billing",1),
 ("Agile delivery core: 2-week sprints, product backlog, MoSCoW prioritisation",1),
 ("Why hybrid: fixed-price / fixed-scope needs predictive control; the software build benefits from iterative feedback.",0),
 ("Tailoring & scale: one co-located team, so Scrum/Kanban is enough; a full scaling framework (SAFe / LeSS) would be over-engineering here. If it grew to several teams, scale via Scrum-of-Scrums or an ART.",0)],
 Inches(0.6),Inches(1.2),Inches(5.4),Inches(5.6),size=16)
pic(s,diag_org(),Inches(6.2),Inches(1.2),width=Inches(6.6))
notes(s,"Why hybrid? The commercial side has to be predictive, because the client is buying a fixed price against fixed milestones. But the build itself is software, and software changes as you learn, so inside that wrapper I run two-week agile sprints. On governance: the Project Board owns the budget and the big decisions, assurance sits to the side as an independent check, and the PM runs the three delivery groups day to day.")

# ---- Slide 5: Lifecycle
s=slide(); title_bar(s,"Project Lifecycle")
pic(s,diag_lifecycle(),Inches(0.5),Inches(2.4),width=Inches(12.3))
bullets(s,[("Six phases over six months; agile sprints run inside the Iterative Development phase, with predictive stage-gates between phases.",0)],
 Inches(0.6),Inches(5.4),SW-Inches(1.2),Inches(1.2),size=18)
notes(s,"Six phases. Initiation and Discovery lay the groundwork, then most of the real value gets built during iterative development. After that comes UAT, deployment, and a hypercare period before we formally close. The stage gates between phases are what keep the predictive side honest.")

# ---- Slide 6: Requirements
s=slide(); title_bar(s,"Requirements (Analysis & Design)")
heading(s,"Functional",Inches(0.6),Inches(1.2),Inches(4))
bullets(s,[("SSO login",0),("View timetable",0),("View grades",0),("Unit materials (offline)",0),("Push notifications",0),("Submit / track assignments",0)],Inches(0.6),Inches(1.6),Inches(4),Inches(4.5),size=15)
heading(s,"Non-functional",Inches(4.8),Inches(1.2),Inches(4))
bullets(s,[("Performance: <2s screen load",0),("Availability 99.5%",0),("Security & data-privacy; encryption",0),("Accessibility (WCAG 2.1 AA)",0),("Scalable to peak enrolment",0)],Inches(4.8),Inches(1.6),Inches(4),Inches(4.5),size=15)
heading(s,"Visual design",Inches(9.0),Inches(1.2),Inches(3.8))
bullets(s,[("Murdoch-branded UI kit",0),("Mobile-first layouts",0),("Usability testing with a student cohort",0)],Inches(9.0),Inches(1.6),Inches(3.8),Inches(4.5),size=15)
notes(s,"I've split requirements three ways: functional, non-functional and visual design. The non-functional ones carry a lot of weight. A university client will hold us to availability, load time and accessibility, so I've made those numbers explicit and testable instead of vague.")

# ---- Slide 7: Deliverables
s=slide(); title_bar(s,"Key Deliverables & Acceptance Criteria")
data=[["Phase","Deliverable","Acceptance criteria"],
 ["Initiation","Project charter & plan","Board sign-off"],
 ["Discovery & Design","UX/UI designs + solution architecture","Product Owner sign-off; architecture review passed"],
 ["Iterative Development","App increments (per sprint)","Definition of Done; automated tests pass; demo accepted at sprint review"],
 ["UAT","Tested release candidate","All severity-1/2 defects closed; UAT sign-off"],
 ["Deployment & Go-live","Production release + Systems Manual","Go-live sign-off; manual incl. component inventory, install/config, interface & batch jobs, release notes, backup & DR plan"],
 ["Hypercare & Close","Handover + closure report","Client sign-off; support handover accepted"]]
table(s,data,Inches(0.5),Inches(1.2),Inches(12.3),Inches(5.6),col_w=[Inches(2.3),Inches(4.0),Inches(6.0)],fs=13)
notes(s,"Each phase hands over something concrete, and every deliverable has acceptance criteria attached. That keeps the plan auditable. It also protects us commercially, because the payment milestones only trigger once a deliverable is actually accepted.")

# ---- Slide 8: WBS
s=slide(); title_bar(s,"Work Breakdown Structure (WBS)")
bullets(s,[("1. Project Management & Governance",0),("2. Discovery & Design",0),
 ("3. Development: Frontend / Backend / Integration",0),("4. Quality Assurance & UAT",0),
 ("5. Infrastructure & Deployment",0),("6. Data & Migration",0),
 ("7. Training & Adoption",0),("8. Support (Hypercare)",0)],
 Inches(0.8),Inches(1.4),Inches(7.5),Inches(5),size=20,gap=10)
heading(s,"100% rule",Inches(8.6),Inches(1.5),Inches(4))
bullets(s,[("Every in-scope item maps to exactly one workstream.",0),
 ("Nothing outside the baseline is included.",0),
 ("WBS feeds the schedule, cost and resource plans.",0)],Inches(8.6),Inches(1.9),Inches(4.2),Inches(3),size=15)
notes(s,"The WBS breaks everything down into eight workstreams. The 100 percent rule keeps it honest: all the work is captured, and nothing outside scope creeps in. The schedule, the budget and the staffing all build off this.")

# ---- Slide 9: Gantt
s=slide(); title_bar(s,"Proposed Timeline (Gantt)")
pic(s,diag_gantt(),Inches(0.4),Inches(1.15),width=Inches(12.5))
notes(s,"Here's the six-month schedule. Development is iterative and deliberately overlaps with UAT and migration rather than waiting for a clean handoff. The diamonds are the milestones that matter, and they're the same events that release the payments.")

# ---- Slide 10: Billing
s=slide(); title_bar(s,"Billing Schedule (A$500k fixed price)")
data=[["Milestone","Trigger","%","Amount"],
 ["1. Kick-off","Contract signed, project initiated","25%","A$125,000"],
 ["2. Go-live","Deployed to production (app stores live)","50%","A$250,000"],
 ["3. Closure","Hypercare complete + client sign-off","25%","A$125,000"],
 ["Total","","100%","A$500,000"]]
table(s,data,Inches(0.8),Inches(1.5),Inches(11.7),Inches(3.0),col_w=[Inches(2.4),Inches(5.5),Inches(1.3),Inches(2.5)],fs=16)
bullets(s,[("Commercial basis: fixed price. ~10% contingency reserve held inside the fixed fee.",0),
 ("Milestone payments tie cash flow to accepted, value-delivering events, not elapsed time.",0)],
 Inches(0.8),Inches(4.9),SW-Inches(1.6),Inches(2),size=16)
notes(s,"Billing is milestone-based. The client pays 25% up front to mobilise, half at go-live when they actually get the value, and the final quarter at closure. A contingency reserve sits inside the fixed fee, so overruns are absorbed without going back to the client for more money.")

# ---- Slide 11: Team & resources
s=slide(); title_bar(s,"Team & Resources")
heading(s,"Core delivery team (~9 FTE)",Inches(0.6),Inches(1.2),Inches(6))
bullets(s,[("Vendor Project Manager",0),("Solution Architect",0),("Business Analyst",0),("UX Designer",0),
 ("Tech Lead + 2 Developers",0),("QA / Test Lead",0),("DevOps / Infrastructure",0)],Inches(0.6),Inches(1.6),Inches(6),Inches(4.5),size=16)
heading(s,"Client side",Inches(7.0),Inches(1.2),Inches(5.5))
bullets(s,[("Product Owner",0),("IT / security liaison",0),("Student test group (UAT)",0)],Inches(7.0),Inches(1.6),Inches(5.5),Inches(2.5),size=16)
heading(s,"Staffing profile",Inches(7.0),Inches(3.9),Inches(5.5))
bullets(s,[("Peak staffing during Development (M2–M5).",0),("Ramp-down to support team in Hypercare (M6).",0)],Inches(7.0),Inches(4.3),Inches(5.5),Inches(2),size=16)
notes(s,"About nine people on our side. The client gives us a Product Owner and, crucially, a group of students for UAT, since they're the real users. Staffing is heaviest through development, then tapers to a small support crew for hypercare.")

# ---- Slide 12: Risk
s=slide(); title_bar(s,"Risk & Issue Management")
pic(s,diag_riskmatrix(),Inches(0.4),Inches(1.2),height=Inches(5.7))
data=[["#","Risk","Score","Response"],
 ["R1","Legacy integration harder than expected","20 H","Mitigate: integration spike in Discovery; integration BA"],
 ["R2","Scope creep despite sign-off","12 M","Mitigate: change control; locked baseline"],
 ["R3","Fixed-price cost overrun","15 H","Mitigate: EAC/ETC tracking; 10% reserve; MoSCoW de-scope"],
 ["R4","Key resource unavailable","9 M","Mitigate: cross-skilling; named backups"],
 ["R5","UAT delays / tester availability","9 M","Mitigate: book UAT early; student pool"],
 ["R6","App-store approval delay","6 L","Accept: submit early; follow guidelines"]]
table(s,data,Inches(5.4),Inches(1.3),Inches(7.5),Inches(4.6),col_w=[Inches(0.6),Inches(2.8),Inches(0.9),Inches(3.2)],fs=11)
bullets(s,[("Issue log: ID · description · severity · owner · status · resolution date (e.g., I1 · SSO test environment unavailable · High · Tech Lead · Open · target M2).   Risk responses: Mitigate / Avoid / Transfer / Accept / Contingency.",0)],
 Inches(5.4),Inches(6.1),Inches(7.5),Inches(1),size=12)
notes(s,"Risks are scored likelihood times consequence, so the worst combinations rise to the top. Three land in the high band: legacy integration, cost overrun and scope creep. Integration worries me most, so I'd spend the proof-of-concept money in week two, before we're locked in. Cost is held in check by tracking EAC and ETC, by the contingency reserve, and by being willing to drop the 'could-haves' with MoSCoW.")

# ---- Slide 13: Stakeholder
s=slide(); title_bar(s,"Stakeholder Management")
pic(s,diag_mendelow(),Inches(0.4),Inches(1.15),height=Inches(5.0))
heading(s,"Communication plan",Inches(8.7),Inches(1.3),Inches(4.2))
bullets(s,[("Weekly RAG status → PM / Board",0),("Fortnightly sprint review → stakeholders",0),
 ("Monthly steering committee",0),("Go-live comms campaign → students",0)],Inches(8.7),Inches(1.75),Inches(4.3),Inches(3.5),size=15)
notes(s,"I've mapped stakeholders by how much power and interest each has. The Board and Product Owner I manage closely. Students and lecturers care a lot but don't control the project, so they're the group I keep informed. The plan just sets how often each group hears from me.")

# ---- Slide 14: Monitoring & control
s=slide(); title_bar(s,"Monitoring & Control")
heading(s,"Schedule & scope",Inches(0.6),Inches(1.2),Inches(6))
bullets(s,[("Weekly RAG status board",0),("Fortnightly sprint burndown + reviews",0),("Milestone tracking against baseline",0),
 ("Change control: every request impact-assessed vs baseline, Board-approved",0)],Inches(0.6),Inches(1.6),Inches(6.1),Inches(3),size=15)
heading(s,"Commercial control (EVM-style · illustrative)",Inches(7.0),Inches(1.2),Inches(5.8))
data=[["Field","Value"],["Commercial basis","Fixed price"],["Budget at Complete (BAC)","A$500k"],
 ["Actual cost to date","A$40k"],["Percent complete","8%"],["Estimate to Complete (ETC)","A$460k"],
 ["Estimate at Complete (EAC)","A$500k"],["Budget variance","A$0"],["Forecast finish","Month 6"]]
table(s,data,Inches(7.0),Inches(1.6),Inches(5.6),Inches(4.4),col_w=[Inches(3.2),Inches(2.4)],fs=14)
notes(s,"Control runs on two fronts. On schedule, it's the weekly RAG board and the sprint burndowns. On money, the commercial table tracks budget against actuals and forecast, so cost drift shows up early instead of at the end. Change control is what stops the fixed-price baseline quietly eroding.")

# ---- Slide 15: Success & closure
s=slide(); title_bar(s,"Success Factors & Closure")
heading(s,"Success factors",Inches(0.6),Inches(1.2),Inches(6))
bullets(s,[("Stakeholder alignment & sponsor engagement",0),("Early de-risking of integration",0),
 ("Disciplined change control",0),("Agile prioritisation (MoSCoW)",0),("Continuous UAT",0),("Clear governance & reporting",0)],
 Inches(0.6),Inches(1.6),Inches(6),Inches(4.5),size=16)
heading(s,"Closure",Inches(7.0),Inches(1.2),Inches(5.8))
bullets(s,[("Client sign-off",0),("Handover to support / BAU",0),("Final reports + lessons learned",0),
 ("System closure",0),("Final invoice (milestone 3)",0)],Inches(7.0),Inches(1.6),Inches(5.8),Inches(4.5),size=16)
notes(s,"If I had to name what makes or breaks this: stakeholder alignment, tackling the integration risk early, and not letting scope drift. Closure itself is simple. The client signs off, we hand over to support, write up lessons learned, and raise the final invoice.")

# ---- Slide 16: References
s=slide(); title_bar(s,"References")
bullets(s,[("Project Management Institute. 2021. A Guide to the Project Management Body of Knowledge (PMBOK Guide). 7th ed. Newtown Square, PA: PMI.",0),
 ("Project Management Institute. 2017. Agile Practice Guide. Newtown Square, PA: PMI.",0),
 ("Figures (lifecycle, org chart, Gantt, risk matrix, stakeholder interest–influence map): author's own work.",0)],
 Inches(0.7),Inches(1.5),SW-Inches(1.4),Inches(4.5),size=16,gap=12)
notes(s,"References follow Chicago style. The frameworks come from PMBOK 7th edition and the Agile Practice Guide. Stakeholders are mapped on an interest–influence grid, the approach used in class. All figures are my own.")

path=os.path.join(OUT,"BUS363_A2_Project_Plan_LMS_App.pptx")
prs.save(path)
print("SAVED:",path)
print("Slides:",len(prs.slides._sldIdLst))
