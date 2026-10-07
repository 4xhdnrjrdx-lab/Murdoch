import fs from 'node:fs/promises';
import path from 'node:path';
import {pathToFileURL} from 'node:url';
import {Presentation, PresentationFile, FileBlob} from '@oai/artifact-tool';

const skill='/Users/king1/.codex/plugins/cache/openai-primary-runtime/presentations/26.921.11914/skills/presentations';
const workspaceDir='/Users/king1/Documents/Murdoch/BUS219/Poland_case_2026-09-22';
const tmp=path.join(workspaceDir,'.build');
const {resolvePresentationFont,finalizePresentation}=await import(pathToFileURL(path.join(skill,'container_tools/artifact_tool_utils.mjs')).href);
const family=resolvePresentationFont();
const p=Presentation.create({slideSize:{width:1280,height:720}});
const s=p.slides.add();
s.background.fill='#FFFFFF';
function text(name,content,x,y,w,h,size,color='#222222',bold=false){
  const a=s.shapes.add({name,geometry:'textbox',position:{left:x,top:y,width:w,height:h},fill:'none',line:{fill:'none',width:0}});
  a.text=content;
  a.text.style={typeface:family,fontSize:size,color,bold,autoFit:'none'};
  return a;
}
text('title','Poland: a new factory near Warsaw',66,42,1148,72,49,'#202020',true);
text('subtitle','A Canadian company plans to make small power tools',68,124,1138,42,27,'#616161');
text('q1','1. Business climate',68,199,530,45,30,'#A82131',true);
text('a1','The case describes skilled workers and good transport. In 2026, rising energy costs and difficulty finding staff are concerns.',68,252,530,145,27);
text('q2','2. Main reason to invest',68,421,530,45,30,'#A82131',true);
text('a2','An economic approach: the firm expects lower costs and profits from selling tools across the region.',68,474,530,138,27);
text('q3','3. Checks before investing',671,199,536,45,30,'#A82131',true);
text('a3','Ask buyers what they need. Compare competitors, prices and costs. Check local rules. This helps test whether the plan can work.',671,252,536,145,27);
text('q4','4. What would make it work',671,421,536,45,30,'#A82131',true);
text('a4','Reliable tools at affordable prices, local sales and repair support, and enough profit after costs. Test demand before expanding.',671,474,536,145,27);
text('source','Sources: Poland case, p. 305; European Commission, Poland forecast, 21 May 2026',68,666,1135,26,16,'#686868');
const speech=`This case is about a Canadian company planning to make power tools near Warsaw.

First, Poland looks attractive because of its skilled workers and good transport. Today, higher energy costs and finding enough staff are concerns.

Second, the company is using an economic approach. It expects lower costs and hopes to make a profit by selling tools across the region.

Before investing, it should talk to buyers, compare competitors and prices, and check costs and local rules. This would help it avoid spending money on a factory without enough customers.

To succeed, it needs reliable tools, affordable prices and local sales and repair support. I would start small and test demand before expanding.`;
s.speakerNotes.textFrame.setText(speech+'\n\nSources\nLocal case: In the International Spotlight: Poland, page 305, course PDF. The scenario contains figures from 2012. The proposed investment and expected lower costs are case assumptions, not independently verified current market facts.\n2026 update for Question 1: European Commission, Economic forecast for Poland, 21 May 2026. https://economy-finance.ec.europa.eu/economic-surveillance-eu-member-states/country-pages-including-country-reports/poland/economic-forecast-poland_en\nQuestion 3: environmental scanning means gathering and checking information about customers, competitors, costs and rules before deciding. Question 2 uses an economic imperative approach; political incentives and product quality support the plan but are not its main motive.');
const candidatePath=path.join(tmp,'candidate.pptx');
await (await PresentationFile.exportPptx(p)).save(candidatePath);
const finalPath=path.join(workspaceDir,'output','BUS219_Poland_Faiaz_One_Slide.pptx');
await finalizePresentation({workspaceDir,candidatePath,finalPath,pythonExecutable:'/Users/king1/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3',integrityValidatorPath:path.join(skill,'container_tools/inspect_presentation_package_integrity.py'),layoutValidatorPath:path.join(skill,'container_tools/inspect_presentation_layout_geometry.py'),layoutArgs:['--expected-slide-size-emu','12192000,6858000','--validate-bullet-geometry','--validate-heading-fit'],explicitTotalSlideCount:1,requiredNativeTableOwnerSlides:[],requiredNativeChartOwnerSlides:[],fontPolicy:{basis:'design',families:[family]},verifyArtifactToolImport:true,receiptPath:path.join(tmp,'validation.json')});
const final=await PresentationFile.importPptx(await FileBlob.load(finalPath));
const preview=await final.export({slide:final.slides.items[0],format:'png',scale:1});
await fs.writeFile(path.join(tmp,'slide-final.png'),new Uint8Array(await preview.arrayBuffer()));
await fs.writeFile(path.join(workspaceDir,'output','Poland_speaking_notes.md'),'# Poland case\n\n## Что сказать на английском\n\n'+speech+'\n\n## Смысл по-русски\n\nКанадская компания хочет открыть производство электроинструментов возле Варшавы. В кейсе Польшу считают удобным местом из-за работников и транспорта. По свежим данным, расходы на энергию растут, а найти сотрудников может быть непросто.\n\nКомпания прежде всего рассчитывает снизить расходы и заработать. Перед вложениями ей нужно поговорить с покупателями и проверить конкурентов, цены, расходы и правила. Это поможет понять, хватит ли клиентов. Для успеха нужны надёжные инструменты по доступной цене, местные продавцы и ремонт. Лучше сначала проверить спрос на небольшом объёме.\n\n## Если преподаватель уточнит термины\n\nEconomic imperative: компания выбирает вариант, который поможет снизить расходы и получить прибыль.\n\nEnvironmental scanning: сбор информации о покупателях, конкурентах и условиях работы перед решением. Здесь это анализ деловой среды, а не только природы или экологии.\n\n## Источники\n\nКейс Poland, страница 305, из материалов BUS219. Данные о 2012 годе относятся к периоду кейса.\n\nОбновление для первого вопроса: [European Commission, Economic forecast for Poland, 21 May 2026](https://economy-finance.ec.europa.eu/economic-surveillance-eu-member-states/country-pages-including-country-reports/poland/economic-forecast-poland_en).\n');
console.log(JSON.stringify({finalPath,font:family,preview:path.join(tmp,'slide-final.png'),speechWords:speech.split(/\s+/).length}));
