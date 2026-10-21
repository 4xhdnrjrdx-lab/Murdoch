import json, shutil
from pathlib import Path

ROOT=Path('/Users/king1/Documents/Murdoch')
OUT=ROOT/'BUS230/2026-TSD/Assignments/A2/Redesign_2026-10-21'
old=json.loads((ROOT/'BUS230/2026-TSD/Assignments/A2/Complete_2026-10-14/Sources/Slide_Content_and_Notes_EN.json').read_text())
slides=old['slides'][:18]
titles={2:'The management session',3:'Cedar Retail: the change',4:'Three manager objectives',6:'ADKAR and the wider method',7:'01 / Shared working conditions',8:'02 / A reasonable objection',9:'03 / Dependencies across roles',10:'Four limitations, four additions',11:'Our modified decision tool',12:'Conditions and concerns',13:'The dependency register',14:'One complete decision record',15:'Implementation and owners',16:'Continue, revise or pause',17:'Feasibility and evaluation',18:'Risks and practical safeguards'}
for s in slides:
 s['original_body']=s['body'];s['title']=titles.get(s['number'],s['title'])

refs=[r for s in old['slides'][28:30] for r in s['body']]
aramrefs=[r for r in refs if r.startswith(('Edmondson,','Morrison,','Kluger,','Baldwin,','Lewis,'))]

new=[
dict(number=19,title='Beyond the ADKAR Score',kind='evidence',seconds=60,presenter='Aram',
 body=[['SELF-REPORT','“I understand the procedure.”'],['TASK DEMONSTRATION','Can the employee do it?'],['WORKING CONDITIONS','Can the task be done here?']],
 takeaway='If evidence conflicts, readiness is NOT YET VERIFIED.',
 cites='Baldwin and Ford 1988; Kluger and DeNisi 1996',
 notes='''An ADKAR score is a useful starting point, but it is not the whole decision. A colleague may report that they understand the change and feel ready. We still need to see whether they can perform the task, with the equipment and time that the job requires.

Our fourth addition is the Evidence Disagreement Rule. If self-report, task performance and working conditions conflict, readiness is not yet verified. The manager investigates the difference instead of averaging it away.

This rule is our team’s proposal, not an official Prosci feature. It has not been scientifically validated. Let us make the distinction between Knowledge and Ability clear.''',
 cue='00:00–01:00. Speak for about 55 seconds; leave 5 seconds for the transition.'),
dict(number=20,title='Knowing Is Not the Same as Doing',kind='knowledge',seconds=60,presenter='Aram',
 body=[['KNOWLEDGE','Understands the procedure\nCan explain the steps'],['ABILITY','Performs the task correctly\nUses real equipment\nWorks in realistic conditions']],
 takeaway='Knowledge must be explained. Ability must be demonstrated.',
 cites='Baldwin and Ford 1988; Edmondson 1999',
 notes='''At Cedar Retail, the employee can explain how to receive a delivery, scan the items and report a stock mismatch. That gives us evidence of Knowledge. It does not yet demonstrate Ability.

For Ability, we need a realistic task: use the actual scanner, receive a sample delivery and report a mismatch correctly. Reliable equipment, protected practice time and a safe learning setting make that demonstration possible.

Baldwin and Ford help us think about transfer from training to work. Edmondson helps explain why people need to feel safe to discuss mistakes and learn.

Our takeaway is simple: Knowledge must be explained. Ability must be demonstrated. Now you will apply that distinction.''',
 cue='01:00–02:00. Point to Knowledge, then Ability. Do not claim that an explanation proves complete Knowledge.'),
dict(number=21,title='Now It’s Your Turn!',kind='workshop',seconds=45,presenter='Aram',
 body=[['WELCOME TO CEDAR RETAIL','Management Training'],['YOUR ROLE','Your team is now responsible for making a management decision.']],
 takeaway='Listen. Ask. Respond without blame.',
 cites='Lewis 1999; Morrison 2023; Edmondson 1999',
 notes='''Before the activity, one communication point matters. We need to listen to employees, invite questions and explain how their concerns affect our decisions. People should be able to discuss a problem without being blamed for raising it.

Welcome to Cedar Retail Management Training. Your team is now responsible for making a management decision.

Could our volunteer group join the discussion from your seats? You do not need to come to the front. There is no pressure to get the answer right. We want to hear your reasoning.''',
 cue='02:00–02:45. Invite the volunteer group from their seats. Do not claim participation happened in advance. If unavailable, invite silent individual reflection and use the backup on slide 22.'),
dict(number=22,title='You Are the Manager',kind='challenge',seconds=120,presenter='Aram',
 body=[['01','The scanner is unreliable.'],['02','There is no protected practice time.'],['03','The employee fears unfair penalties for previous stock errors.']],
 takeaway='WHAT WOULD YOUR TEAM DECIDE?',cites='Fictional Cedar Retail scenario · Apply our proposed decision rules',
 notes='''Cedar Retail is introducing a digital inventory system. An evening-shift employee understands the procedure. However, the scanner is unreliable, there is no protected practice time, and the employee fears unfair penalties for previous stock errors. The manager suggests another motivational talk.

What would your team decide: A, Continue; B, Revise; or C, Pause? You have thirty seconds to discuss. Please choose one decision and explain why.

[STOP SPEAKING. Allow 30 seconds of discussion.]

Which decision did you choose? Could one person briefly explain your reason?

[LISTEN. Allow one participant up to 30 seconds.]

Thank you for explaining your thinking. Let us compare that with the evidence-based decision.''',
 cue='''02:45–04:45. Two-minute activity: 00–25 scenario; 25–40 question and instructions; 40–70 discussion (30 seconds); 70–80 invite one answer; 80–110 answer or backup; 110–120 thank, select the chosen card and reveal slide 23. Use a presenter clock; the deck does not run an automatic countdown.

IF A / CONTINUE: “Thank you. You want to keep the change moving. What happens if the scanner fails during the task? Let us check whether the essential conditions are ready.”
IF B / REVISE: “Thank you. Reviewing the penalty rule matters. We also need to decide what happens to the affected task while equipment and practice time are still missing.”
IF C / PAUSE: “Thank you. Let us check the scope of the pause and what would allow the task to restart.”
IF NO ANSWER OR NO VOLUNTEERS: Wait briefly, then say: “Let us reason it through together. The procedure is understood, but two essential conditions are missing. I would pause the affected task while the owners address those conditions and the sponsor reviews the concern.”
Only speak the relevant branch. Shorten the final thanks if needed to finish at 02:00. Any A/B/C button opens the same worked answer. It does not record or judge the chosen answer.'''),
dict(number=23,title='The Evidence-Based Decision',kind='reveal',seconds=75,presenter='Aram',
 body=[['IT LEAD','Provide reliable scanner access.'],['STORE MANAGER','Arrange protected practice time.'],['OPERATIONS SPONSOR','Review the penalty policy; communicate a reasoned decision.'],['MANAGER','Observe a realistic task to verify Ability.']],
 takeaway='A motivational talk alone cannot solve missing organisational conditions.',
 cites='Baldwin and Ford 1988; Kluger and DeNisi 1996; Morrison 2023',
 notes='''Our recommended answer is C: pause the affected task. This does not mean stopping the entire change project. The employee can still learn the procedure while the team fixes the conditions needed for this task.

The IT Lead provides reliable scanner access. The Store Manager arranges protected practice time. The Operations Sponsor reviews the disputed penalty policy and communicates a reasoned decision. If the rule unfairly penalises inherited errors, it needs revision; the review should establish that, rather than assume the facts.

After these conditions are addressed, the manager observes a realistic task to verify Ability. Policy revision matters, but the task stays paused until its essential prerequisites are met.

A motivational talk alone cannot solve missing organisational conditions. The response needs named owners, practical action and a new evidence check.''',
 cue='04:45–06:00. Reveal after hearing the group. Emphasise task-level scope. Restart only after prerequisites and task evidence are verified. Do not invent completed scanner repairs, sponsor approval or a successful demonstration.'),
dict(number=24,title='From ADKAR Scores to Better Decisions',kind='closing',seconds=60,presenter='Aram',
 body=[['01','Identify individual ADKAR barriers.'],['02','Check organisational conditions.'],['03','Listen and respond to employee concerns.'],['04','Verify real workplace performance.']],
 takeaway='DON’T ASSUME READINESS.\nVERIFY IT.',
 cites='Team synthesis · Proposed adaptation; effectiveness remains untested',
 notes='''To conclude our group presentation, keep four principles in mind.

First, identify the individual ADKAR barrier and provide relevant support. Second, check the organisational conditions needed for the actual task. Third, listen to employee concerns and provide a reasoned response. Fourth, verify real workplace performance before assuming readiness.

We keep ADKAR’s useful language and add explicit owners, dependencies and an evidence-based task decision. Our record is a teaching proposal. Its usefulness still needs to be tested in practice.

The next step for a manager is to try the record on one task, review what happens and improve it.

Don’t assume readiness. Verify it. Thank you. We are happy to take your questions.''',
 cue='06:00–07:00. End the seven-minute block here. In the full team session, 21 minutes for presenters 1–3 plus 7 minutes here leaves up to 2 minutes for questions. Actual delivery time requires rehearsal. Do not read sources aloud.')]

for s in new:
 s['references']=aramrefs
slides+=new
for j in range(4):
 slides.append(dict(number=25+j,title=f'Academic references / {j+1:02}',kind='references',body=refs[j*5:(j+1)*5],cites='Chicago 17 author-date · 20 academic publications across four slides',notes='Reference display; do not read aloud. Retained from the source pack. Source access and evidence limits remain as documented in Complete_2026-10-14/BUS230A2_Research_and_References_EN_2026-10-14.pdf.',seconds=0,presenter='Appendix'))
slides.append(dict(number=29,title='Research and evidence boundaries',kind='boundaries',body=[['ADKAR','Diagnoses individual support needs.','The five outcomes alone are not a project plan.'],['Wider Prosci','Adds sponsorship, project health and process.','Existing provisions deserve credit.'],['Research literature','Informs context, voice, transfer and evaluation.','Evidence comes from different settings.'],['Our proposed record','Makes owners and decision evidence explicit.','Usability and effectiveness need testing.']],cites=old['slides'][18]['cites']+'; Nilsen 2015; Prosci n.d.-b, n.d.-c',notes=old['slides'][18]['notes']+'\n\n'+old['slides'][21]['notes']+'\n\nBenchmarking here means comparison with research-informed design criteria, not evidence that Cedar Retail is a real company or that a field evaluation has been conducted. Full sources for the original model and acknowledgements:\n'+old['slides'][27]['notes'],seconds=0,presenter='Appendix'))
slides.append(dict(number=30,title='Communication and manager workflow',kind='communication',body=old['slides'][23]['body'],cites=old['slides'][23]['cites'],notes=old['slides'][22]['notes']+'\n\n'+old['slides'][23]['notes']+'\n\nProfessional and course source acknowledgements:\n'+old['slides'][27]['notes'],seconds=0,presenter='Appendix'))

slides[17]['notes']+='\n\nResearch transition: Stouten, Rousseau and De Cremer (2018) compare change-management advice with the scholarly literature. Errida and Lotfi (2021) identify broader success factors. We use that literature to justify fields for diagnosis, conditions, participation and review; it does not validate our proposed record. Further research comparisons are retained in appendix slide 29. Aram now demonstrates the evidence rule.'

data={**old,'prepared_on':'2026-10-21','slide_count':30,'target_seconds':1800,'main_sequence':24,'appendix_slides':[25,26,27,28,29,30],'slides':slides,'revision_note':'Full visual redesign requested; Aram 19–24 follows the user-supplied seven-minute brief. Appendix retains research comparisons, stakeholder plan and all 20 academic references. Appendix hidden during normal slide show. First 18 speeches retained. Core timing 28 minutes; questions up to 2 minutes. No actual rehearsal claimed.'}
(OUT/'Sources/Slide_Content_and_Notes_EN.json').write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')

lines=['# Aram: speaker notes and offline activity','', 'Slides 19–24 · planned total 7:00, including the two-minute activity. This is a timed rehearsal plan; delivery speed and the group’s response must be rehearsed.','', '| Slide | Duration | Block clock |','|---|---|---|','|19|1:00|0:00–1:00|','|20|1:00|1:00–2:00|','|21|0:45|2:00–2:45|','|22|2:00|2:45–4:45|','|23|1:15|4:45–6:00|','|24|1:00|6:00–7:00|','', '## Operating the activity','', 'Open the PPTX in Slide Show mode. On slide 22, let the volunteer group discuss from their seats for 30 seconds. Hear one answer. Click its A, B or C card to open the same worked answer on slide 23; the choice is not stored. The space bar or right arrow also advances to the answer. The answer slide links back to the challenge and forward to the conclusion. No internet, polling app or macro is required. There is no automatic countdown. Use the presenter clock.','', 'When copying into another deck, insert the six slides as a block and choose Keep Source Formatting. PowerPoint may rewrite slide links during copying: test the three cards after insertion. Right-arrow navigation is the fallback.','']
for s in new:lines+=['## Slide '+str(s['number'])+' — '+s['title'],'','### Say this','',s['notes'],'','### Presenter cues (do not read aloud)','',s['cue'],'','### Short citation','',s['cites'],'']
lines+=['## Full academic references','']+['- '+r for r in aramrefs]
(OUT/'Aram_Speaker_Notes_EN.md').write_text('\n'.join(lines)+'\n')
allnotes=['# Team speaker notes','', 'Core slides 1–24: 28-minute budget. Up to two minutes for questions. Appendix slides 25–30 are hidden in the slide show. The first three speakers retain their original seven-minute speeches.','']
for s in slides:
 allnotes+=['## '+str(s['number'])+' — '+s['title'],'',f"Presenter: {s['presenter']}. Budget: {s['seconds']} seconds.",'',s['notes'],'',s.get('cue',''),'','Sources: '+s['cites'],'']
(OUT/'Team_Speaker_Notes_EN.md').write_text('\n'.join(allnotes)+'\n')
print('Prepared',len(slides),'slides;',sum(s['seconds'] for s in slides),'seconds core, plus 120 seconds Q&A')
