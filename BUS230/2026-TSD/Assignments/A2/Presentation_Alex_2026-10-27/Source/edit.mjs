import fs from 'node:fs/promises';
import {FileBlob,PresentationFile} from '@oai/artifact-tool';
const root='/private/tmp/bus230-alex-demo-20261027';
const source='/private/tmp/murdoch-bus230-scripts-20261027/BUS230/2026-TSD/Assignments/A2/Presentation_QR_2026-10-27/BUS230Assessment2Class2Group4_2026-10-27_QR.pptx';
const p=await PresentationFile.importPptx(await FileBlob.load(source)); const s=p.slides.items[24];
for(const sh of [...s.shapes.items])if(['text-24','text-25','text-26','text-27','text-28','text-29','text-30','text-31','game-link-label','game-url'].includes(sh.name))sh.delete();
function label(name,text,pos,size,bold=false,color='#202020',align='left'){const sh=s.shapes.add({name,geometry:'textbox',position:pos,fill:'none',line:{fill:'none',width:0}});sh.text=text;sh.text.insets=0;sh.text.style={typeface:'Avenir Next',fontSize:size,bold,color,alignment:align};return sh;}
label('alex-demo-heading','ALEX: PRACTICE EXAMPLE / 36 SECONDS',{left:64,top:145,width:730,height:35},22,true,'#FF5500');
const bytes=await fs.readFile(root+'/build/poster.png');s.images.add({name:'alex-video-poster',blob:bytes.buffer.slice(bytes.byteOffset,bytes.byteOffset+bytes.byteLength),contentType:'image/png',alt:'Play the separate Alex practice demonstration, 36 seconds',fit:'contain',position:{left:64,top:190,width:704,height:396}});
label('team-instructions','One phone per team of four. Review all five colleagues.\nFour minutes, then tap Finish & send review.',{left:64,top:598,width:710,height:58},21);
label('team-options','Team 1, 2 or 3 / Others',{left:840,top:552,width:380,height:36},23,false,'#202020','center');
label('game-url','cedar-retail-adkar-demo.\nspicy-rhino-0802.chatgpt.site',{left:830,top:598,width:390,height:54},18,false,'#666561','center');
const notes=JSON.parse(await fs.readFile(root+'/build/Aram_Notes.json','utf8'));
for(const [n,text] of Object.entries(notes))p.slides.items[Number(n)-1].speakerNotes.text=text;
await(await PresentationFile.exportPptx(p)).save(root+'/build/edited-roundtrip.pptx');
for(const n of [24,25,26]){const b=await p.export({slide:p.slides.items[n-1],format:'png',scale:1});await fs.writeFile(root+`/build/slide-${n}.png`,new Uint8Array(await b.arrayBuffer()));}
console.log('Artifact Tool layout and notes updated');
