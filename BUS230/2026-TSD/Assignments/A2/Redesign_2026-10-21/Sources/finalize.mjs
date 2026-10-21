import path from 'node:path';
import {finalizePresentation} from '/Users/king1/.codex/plugins/cache/openai-primary-runtime/presentations/26.1017.22135/skills/presentations/container_tools/artifact_tool_utils.mjs';
const SK='/Users/king1/.codex/plugins/cache/openai-primary-runtime/presentations/26.1017.22135/skills/presentations';
const OUT='/Users/king1/Documents/Murdoch/BUS230/2026-TSD/Assignments/A2/Redesign_2026-10-21';
process.env.RUNTIME_NODE_MODULES='/Users/king1/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules';
process.env.RUNTIME_NODE='/Users/king1/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node';
for(const [name,count,tables,file] of [['full',30,[5,10,12,13,14,15,18,29,30],'BUS230Assessment2Class2Group4_2026-10-21.pptx'],['aram',6,[],'BUS230A2_Aram_Slides19-24_2026-10-21.pptx']]){
 const r=await finalizePresentation({workspaceDir:'/private/tmp/bus230-redesign-build',candidatePath:'/private/tmp/bus230-redesign-build/'+name+'-linked.pptx',finalPath:'/private/tmp/bus230-redesign-build/output/linked-final-'+file,pythonExecutable:'/Users/king1/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3',integrityValidatorPath:SK+'/container_tools/inspect_presentation_package_integrity.py',layoutValidatorPath:SK+'/container_tools/inspect_presentation_layout_geometry.py',layoutArgs:['--expected-slide-size-emu','12192000,6858000','--validate-bullet-geometry','--validate-heading-fit',...tables.flatMap(n=>['--require-native-table-slide',String(n)])],explicitTotalSlideCount:count,requiredNativeTableOwnerSlides:tables,requiredNativeChartOwnerSlides:[],fontPolicy:{basis:'design',families:['Avenir Next']},verifyArtifactToolImport:true,receiptPath:'/private/tmp/bus230-redesign-build/'+name+'-linked-final-validation.json'});
 console.log(name,JSON.stringify(r));
}
