import fs from 'node:fs/promises';
import {FileBlob,PresentationFile} from '@oai/artifact-tool';
const dir='/private/tmp/bus230-qr-20261027',source='/private/tmp/murdoch-bus230-scripts-20261027/BUS230/2026-TSD/Assignments/A2/Local_Snapshots_2026-10-27/BUS230Assessment2Class2Group4_2026-10-26_LOCAL_SNAPSHOT_2026-10-27.pptx';
const p=await PresentationFile.importPptx(await FileBlob.load(source)),s=p.slides.items[24];
p.resolve('im/a9gjmx4j').delete();
s.background.fill='#F1F0EC';
for(const id of ['sh/h0jalgra','sh/uxsra18j'])p.resolve(id).delete();
function replace(id,text){p.resolve(id).text=text;}
replace('sh/29wby1wf','TEAM 1 / TEAM 2 / TEAM 3 / OTHERS');
replace('sh/pc7atgf6','Choose your team. Guests choose Others.');
replace('sh/wza9cbqp','Review all five, then tap Finish & send review.');
function label(name,text,pos,size,bold=false,color='#202020',align='left'){
 const shape=s.shapes.add({name,geometry:'textbox',position:pos,fill:'none',line:{fill:'none',width:0}});shape.text=text;shape.text.insets=0;shape.text.style={typeface:'Avenir Next',fontSize:size,bold,color,alignment:align};return shape;
}
label('qr-heading','SCAN TO PLAY',{left:850,top:146,width:370,height:40},24,true,'#FF5500','center');
const bytes=await fs.readFile(dir+'/build/Cedar_Retail_Game_QR.png');
s.images.add({name:'game-qr',blob:bytes.buffer.slice(bytes.byteOffset,bytes.byteOffset+bytes.byteLength),contentType:'image/png',alt:'Scan to open the Cedar Retail office game',fit:'contain',position:{left:860,top:190,width:352,height:352}});
label('game-link-label','Scan with your phone',{left:850,top:562,width:370,height:38},23,false,'#202020','center');
label('game-url','https://cedar-retail-adkar-demo.spicy-rhino-0802.chatgpt.site/',{left:64,top:616,width:1135,height:32},20,false,'#666561');
const notes=JSON.parse(await fs.readFile(dir+'/build/Aram_Notes.json','utf8'));
for(const [n,text] of Object.entries(notes)){p.slides.items[Number(n)-1].speakerNotes.text=text;}
await (await PresentationFile.exportPptx(p)).save(dir+'/build/edited-roundtrip.pptx');
for(const n of [24,25,26]){const b=await p.export({slide:p.slides.items[n-1],format:'png',scale:1});await fs.writeFile(dir+`/build/after-${n}.png`,new Uint8Array(await b.arrayBuffer()));}
console.log('Edited slide 25 and Aram speaker notes with Artifact Tool');
