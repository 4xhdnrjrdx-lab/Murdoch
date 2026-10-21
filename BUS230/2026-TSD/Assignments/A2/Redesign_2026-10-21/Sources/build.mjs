import fs from 'node:fs/promises';
import path from 'node:path';
import {Presentation,PresentationFile} from '@oai/artifact-tool';

const ROOT='/Users/king1/Documents/Murdoch';
const OUT=ROOT+'/BUS230/2026-TSD/Assignments/A2/Redesign_2026-10-21';
const BUILD='/private/tmp/bus230-redesign-build';
const data=JSON.parse(await fs.readFile(OUT+'/Sources/Slide_Content_and_Notes_EN.json','utf8'));
const artwork=new Uint8Array(await fs.readFile(OUT+'/Sources/Editorial_Background.png'));
const C={bg:'#F1F0EC',ink:'#202020',orange:'#FF5500',muted:'#666561',line:'#CCCAC5',green:'#176C50',amber:'#A86B00',red:'#BF352A',white:'#FFFFFF'};
const FONT='Avenir Next';
let id=0;
function shape(s,geo,x,y,w,h,fill=C.ink,name){return s.shapes.add({name:name??`shape-${++id}`,geometry:geo,position:{left:x,top:y,width:w,height:h},fill,line:{fill:'none',width:0}})}
function text(s,str,x,y,w,h,size=28,color=C.ink,bold=false,align='left',name){const t=shape(s,'textbox',x,y,w,h,'none',name);t.text=str;t.text.style={typeface:FONT,fontSize:size,color,bold,alignment:align,verticalAlignment:'top',wrap:'square',autoFit:'none',insets:0};return t;}
function line(s,x,y,w,color=C.line){const l=shape(s,'line',x,y,w,0,'none');l.line={fill:color,width:1};return l;}
function node(s,label,x,y,d,fill=C.orange,size=38,color=C.ink){const n=shape(s,'ellipse',x,y,d,d,fill);n.text=label;n.text.style={typeface:FONT,fontSize:size,bold:true,color,alignment:'center',verticalAlignment:'middle',insets:6};return n;}
function banner(s,str,y=590,size=31,color=C.orange){text(s,str,64,y,1150,80,size,color,true);}
function base(p,d){const s=p.slides.add();s.background.fill=C.bg;
 if(![1,21].includes(d.number)){
 text(s,d.title,64,54,1145,138,d.number===24?43:49,C.ink,false,'left','slide-title');
 text(s,String(d.number).padStart(2,'0'),1177,661,45,24,18,C.ink,false,'right','slide-number');
 text(s,d.cites,64,661,1090,35,14.5,C.muted);
 }
 const refs=d.references??[];
 s.speakerNotes.text=`${d.presenter} · Slide ${d.number} · Planned budget ${d.seconds} seconds\n\nSAY THIS\n${d.notes}\n\nPRESENTER CUES — DO NOT READ ALOUD\n${d.cue??'Use the retained speaker script and the agreed timing budget.'}\n\nSHORT SOURCES\n${d.cites}\n\nFULL REFERENCES / SOURCE BOUNDARIES\n${refs.join('\n\n')}\n\nSource basis: A2_ADKAR_TEAM_PLAN_EN_2026-10-14.pdf and the 14 October full preparation pack. Cedar Retail is fictional. No study of the proposed adaptation, actual rehearsal or completed management action is claimed.`;
 return s;}
function table(s,values,y=219,widths=null,font=24,height=366){const cols=values[0].length;
 const t=s.tables.add({rows:values.length,columns:cols,left:64,top:y,width:1152,height,values,columnWidths:widths??Array(cols).fill(1152/cols)});
 t.borders.assign({fill:C.line,width:.5,style:'solid'});
 for(let r=0;r<values.length;r++)for(let c=0;c<cols;c++){
 const cell=t.getCell(r,c);cell.fill=r===0?C.ink:(r%2===0?'#E7E5E0':C.bg);
 cell.text.style={typeface:FONT,fontSize:r===0?font-1:font,color:r===0?C.white:C.ink,bold:r===0,insets:12,verticalAlignment:'middle',wrap:'square',autoFit:'none'};
 }
 return t;}
function columns(s,items,y=240){const gap=52,w=(1152-gap*(items.length-1))/items.length;
 items.forEach(([head,body],i)=>{let x=64+i*(w+gap);text(s,head,x,y,w,85,30,C.orange,true);text(s,body,x,y+99,w,240,28,C.ink);});}
function flow(s,items,y=245){const xs=[84,462,840];items.forEach(([head,body],i)=>{node(s,String(i+1),xs[i]+72,y,140,i===1?C.ink:C.orange,56,i===1?C.white:C.ink);text(s,head,xs[i]-20,y+168,330,64,27,C.ink,true,'center');text(s,body,xs[i]-20,y+235,330,100,25,C.muted,false,'center');if(i<2)text(s,'→',xs[i]+300,y+38,60,70,54,C.ink);});}
function notesSource(d){const ids=data.sources.filter(r=>d.cites.includes(r.authors?.[0]?.split(' ').at(-1)??'___'));return ids.map(r=>r.citation).filter(Boolean).join('\n\n');}

function make(p,d){const s=base(p,d);let b=d.body;
 if(d.number===1){
  // The generated artwork is an editorial background, not evidence of a real store.
  s.images.add({blob:artwork,contentType:'image/png',alt:'Generated editorial background: black and orange circles, monochrome fictional stockroom',position:{left:0,top:0,width:1280,height:720},fit:'cover'});
  text(s,'BUS230 / ASSESSMENT 2',64,54,570,35,23,C.orange,true);
  text(s,'Using ADKAR\nwith Context\nand Evidence',64,170,620,250,66,C.ink,false);
  text(s,'Formal management training\nClass 2 Group 4 · Murdoch University Dubai',66,455,620,74,24,C.ink);
  text(s,'Mohammad Mazin Mohammad Al Mili · Beryl Soria\nFaiaz Dzhafarov (35553299) · Aram Avetisyan',66,566,650,64,20,C.ink);
  text(s,'Prepared 21 October 2026',66,658,650,30,17,C.muted);
  return s;
 }
 if(d.number===2){
 const items=[['01','Context & objectives'],['02','ADKAR & four limitations'],['03','Our modified decision tool'],['04','Evidence & realistic performance'],['05','Management decision workshop'],['06','Conclusions & questions']];
 items.forEach(([n,v],i)=>{const x=64+(i%2)*604,y=223+Math.floor(i/2)*132;text(s,n,x,y,80,62,44,C.orange);text(s,v,x+97,y+7,430,80,29);line(s,x,y+100,548);});return s;}
 if(d.number===3){
 text(s,'A fictional retailer introduces\ndigital stock receiving.',64,209,690,102,38);
 node(s,'SCAN\nCHECK\nREPORT',896,195,274,C.ink,38,C.white);
 text(s,'THE TASK',64,353,230,42,23,C.orange,true);text(s,'Receive a delivery, identify a stock mismatch\nand report it correctly.',64,400,745,85,29);
 text(s,'THE EVENING SHIFT',64,523,270,40,23,C.orange,true);text(s,'Unreliable scanner · No practice time\nConcern about penalties for inherited errors',64,565,1030,76,28);
 return s;}
 if(d.number===4){flow(s,[['DIAGNOSE','Identify the individual\nADKAR barrier.'],['CONNECT','Name conditions,\nprerequisites and owners.'],['DECIDE','Use evidence to continue,\nrevise or pause.']],215);return s;}
 if(d.number===5){table(s,b,201,[223,445,484],24,404);return s;}
 if(d.number===6){columns(s,[['INDIVIDUAL ADOPTION','ADKAR\n\nShared language\nEarliest barrier\nTargeted support\nRepeated assessment'],['ORGANISATIONAL CHANGE','Wider Prosci Methodology\n\nPCT: success, sponsorship, project health\n3-Phase Process: prepare, manage, sustain']],215);return s;}
 if([7,8,9].includes(d.number)){
 const captions=d.number===7?[['Baseline','Ability may include\nexternal conditions.'],['Standalone gap','Five outcomes do not\nallocate shared ownership.'],['Cedar Retail','IT owns access.\nThe manager owns time.']]:d.number===8?[['Mixed response','Supports better records;\nquestions the penalty rule.'],['Standalone gap','A Desire barrier does not\nrequire a design review.'],['Our addition','Sponsor records a reasoned\nretain, revise or stop decision.']]:[['Personal route','Support the earliest\nindividual ADKAR barrier.'],['Shared work','IT and management resolve\nenabling conditions in parallel.'],['Our addition','Route dependencies\nacross accountable roles.']];
 captions.forEach(([h,body],i)=>{const x=64+i*398;node(s,String(i+1).padStart(2,'0'),x,220,98,i===1?C.ink:C.orange,35,i===1?C.white:C.ink);text(s,h,x,345,345,55,30,C.ink,true);text(s,body,x,417,345,150,28);});return s;}
 if(d.number===10){table(s,b,209,[610,542],26,380);return s;}
 if(d.number===11){flow(s,[['KEEP ADKAR','Individual needs\nand relevant support.'],['ADD CONTEXT','Conditions, concerns,\ndependencies and evidence.'],['RECORD A DECISION','Reason, named owner\nand review trigger.']],211);banner(s,'Our team’s proposed adaptation · effectiveness needs testing',604,25);return s;}
 if(d.number===12){table(s,b,217,[195,648,309],25,371);return s;}
 if(d.number===13){table(s,b,214,[258,320,202,372],23,391);return s;}
 if(d.number===14){
 const vals=[['Record field','Manager question'],...b];table(s,vals,208,[339,813],25,412);return s;}
 if(d.number===15){table(s,b,217,[211,625,316],24,385);return s;}
 if(d.number===16){
 const opts=[['CONTINUE','Prerequisites and task\nevidence verified.','Proceed with support\nand review.',C.green],['REVISE','Design is disputed\nor unsuitable.','Get a reasoned\ndesign decision.',C.amber],['PAUSE','An essential\nprerequisite is missing.','Hold the affected task\nand resolve it.',C.red]];
 opts.forEach(([h,a,z,c],i)=>{let x=64+i*398;node(s,'',x+34,211,244,c,31,C.white);text(s,h,x+34,307,244,50,31,C.white,true,'center');text(s,a,x,484,350,80,28,C.ink,true,'center');text(s,z,x,574,350,67,25,C.muted,false,'center');});return s;}
 if(d.number===17){columns(s,[['PRACTICAL USE','One shared digital PDF record\n\nExisting manager, IT and sponsor roles\n\nEvidence beside each action'],['BENEFITS TO TEST','Task accuracy\nUnresolved dependencies\nReasoned responses\nTime maintaining the record']],220);return s;}
 if(d.number===18){table(s,b,212,[320,832],25,381);return s;}
 if(d.kind==='evidence'){
 flow(s,b,202);banner(s,d.takeaway,592,32);text(s,'Team proposal · not an official Prosci feature',64,158,1000,35,22,C.orange);return s;}
 if(d.kind==='knowledge'){
 node(s,'K',64,209,100,C.orange,53);text(s,'KNOWLEDGE',192,225,390,56,33,C.orange,true);
 node(s,'A',676,209,100,C.ink,53,C.white);text(s,'ABILITY',806,225,355,56,33,C.ink,true);
 line(s,64,329,523);line(s,676,329,540);
 text(s,b[0][1],64,357,535,139,31);text(s,b[1][1],676,357,540,166,31);
 banner(s,d.takeaway,584,31);text(s,'Cedar Retail: digital stock receiving',64,159,1000,36,22,C.muted);return s;}
 if(d.kind==='workshop'){
 s.images.add({blob:artwork,contentType:'image/png',alt:'Editorial background for Cedar Retail training',position:{left:0,top:0,width:1280,height:720},fit:'cover'});
 text(s,d.title,64,60,660,100,59);
 text(s,'WELCOME TO\nCEDAR RETAIL',64,214,625,130,48,C.orange,true);
 text(s,'Management Training',64,356,650,63,38);
 text(s,'Your team is now responsible for\nmaking a management decision.',64,444,620,100,30);
 text(s,'Listen. Ask. Respond without blame.',64,574,640,50,26,C.ink,true);
 text(s,d.cites,64,661,1070,35,14.5,C.muted);text(s,'21',1177,661,45,25,18,C.ink,false,'right');return s;}
 if(d.kind==='challenge'){
 text(s,'Cedar Retail is introducing a digital inventory system.',64,136,1152,44,27);
 text(s,'The employee understands the procedure, but…',64,181,1152,42,25,C.muted);
 b.forEach(([n,z],i)=>{const y=236+i*49;text(s,n,64,y,64,42,28,C.orange,true);text(s,z,145,y,1071,48,27);});
 text(s,'The manager suggests another motivational talk.',64,397,1150,41,26,C.ink);
 text(s,d.takeaway,64,453,1152,50,34,C.ink,true);
 [['A','CONTINUE',C.green],['B','REVISE',C.amber],['C','PAUSE',C.red]].forEach(([n,h,c],i)=>{const a=shape(s,'rect',64+i*398,516,356,94,c,'decision-'+n);a.text=n+' — '+h;a.text.style={typeface:FONT,fontSize:31,color:C.white,bold:true,alignment:'center',verticalAlignment:'middle',insets:10};});
 text(s,'30 seconds to discuss. Choose one decision and explain why.',64,625,1152,35,25,C.ink);return s;}
 if(d.kind==='reveal'){
 text(s,'← Scenario',824,143,176,30,21,C.muted,false,'left','nav-scenario');
 text(s,'Conclusion →',1020,143,196,30,21,C.muted,false,'right','nav-conclusion');
 text(s,'C',64,189,270,161,142,C.orange,true);text(s,'PAUSE THE\nAFFECTED TASK',64,366,337,110,37,C.ink,true);
 text(s,'Keep the wider change\nproject moving.',64,506,337,90,27,C.muted);
 b.forEach(([h,z],i)=>{const y=185+i*101;node(s,String(i+1),442,y,52,i===3?C.ink:C.orange,25,i===3?C.white:C.ink);text(s,h,518,y-1,680,34,23,C.orange,true);text(s,z,518,y+35,680,62,26);});
 banner(s,'A motivational talk alone cannot fix missing conditions.',606,28);return s;}
 if(d.kind==='closing'){
 text(s,'DON’T ASSUME\nREADINESS.',64,224,667,182,64,C.ink,true);text(s,'VERIFY IT.',64,416,650,99,82,C.orange,true);
 b.forEach(([n,z],i)=>{const y=217+i*91;text(s,n,813,y,57,40,25,C.orange,true);text(s,z,883,y,333,85,27);});
 text(s,'Thank you — Questions?',64,581,720,54,36,C.ink);
 return s;}
 if(d.kind==='references'){
 b.forEach((z,i)=>{let y=197+i*88;let clean=z.replaceAll('*','');text(s,clean,64,y,1152,81,20,C.ink);if(i<4)line(s,64,y+82,1152);});return s;}
 if(d.kind==='boundaries'){
 table(s,[['Approach','Contribution','Boundary'],...b],190,[235,461,456],22,367);
 text(s,'Benchmark: diagnosis · enabling conditions · participation · review',64,586,1150,57,27,C.orange,true);return s;}
 if(d.kind==='communication'){
 table(s,b,195,[260,632,260],23,312);
 text(s,'DEFINE → DIAGNOSE → CONNECT → VERIFY → DECIDE & REVIEW',64,553,1152,85,28,C.orange,true);return s;}
 throw new Error('Unhandled '+d.number);
}

async function build(list,name){
 const p=Presentation.create({slideSize:{width:1280,height:720}});p.theme.defaultFont=FONT;
 for(const d of list){const s=make(p,d);if(!d.references){let refs=notesSource(d);s.speakerNotes.append('\n\nACADEMIC REFERENCES\n'+refs);}}
 await fs.mkdir(BUILD+'/'+name,{recursive:true});
 for(const [i,s] of p.slides.items.entries()){
  const png=await p.export({slide:s,format:'png',scale:1});
  await fs.writeFile(BUILD+'/'+name+'/slide-'+String(list[i].number).padStart(2,'0')+'.png',new Uint8Array(await png.arrayBuffer()));
 }
 await (await PresentationFile.exportPptx(p)).save(BUILD+'/'+name+'-draft.pptx');
 await fs.writeFile(BUILD+'/'+name+'-proto.json',JSON.stringify(p.toProto()));
 console.log('Built '+name+' '+p.slides.items.length+' slides');
}
await build(data.slides,'full');
await build(data.slides.slice(18,24),'aram');
