from pathlib import Path
import json
r=Path('/private/tmp/bus230-alex-demo-20261027');src=Path('/private/tmp/murdoch-bus230-scripts-20261027/BUS230/2026-TSD/Assignments/A2/Presentation_QR_2026-10-27/Source');data=json.loads((r/'build/Script_Content_EN.json').read_text());original=json.loads((src/'Aram_Notes.json').read_text());notes={}
data['slides'][23]['speech']+='\n\nBefore the game, watch a separate practice example with Alex.'
s=data['slides'][24];s['speech']='''[The embedded 36-second demonstration starts automatically in Slide Show mode. Read the following while it plays.]

Choose a colleague and read the problem. Alex understands the change, but does not want to take part. Sending the guide again misses his concern. The game explains the mistake and lets us retry. We investigate what would make participation worthwhile, then discuss benefits and invite him to help shape a trial. This can support Desire. We still need to check his willingness.

[When the demonstration ends, continue.]

Now scan the QR code. Use one phone per team of four. Choose Team 1, 2 or 3. Guests choose Others. Visit all five colleagues, then tap Finish and send review. You have four minutes.

[Allow up to 80 seconds in total for the demonstration, narration and joining. Narrate during playback. Then time four minutes of play. Keep this slide visible and host results private. If the embedded animation fails, open the separate MP4, then return to the QR slide. If the site is unavailable, move to slide 26 without inventing submitted results.]'''
s['presenter_cues']=s['presenter_cues'].replace('embedded video','embedded demonstration').replace('It plays on a click','It starts automatically on entering slide 25 in Slide Show mode').replace('36 seconds and has no voice track','36 seconds and has no voice track. It uses a single-play animated GIF of the recorded practice UI for reliable desktop playback. A separate H.264 MP4 is the backup').replace('If video fails, give the short explanation and continue.','If the embedded animation fails, open the separate MP4, then return to the QR slide. If both fail, give the short explanation and continue.')
data['revision']='Alex 36-second practice demonstration on slide 25, 27 October 2026';data['activity_contract']['instruction_demo']='Slide 25, separate Alex Desire case, no audience exercise';data['activity_contract']['demonstration_format']='Single-play animated recording embedded in PPTX; separate 36-second H.264 MP4 backup';data['presentation_source']='BUS230Assessment2Class2Group4_2026-10-27_ALEX.pptx';data['previous_presentation_source']='../Presentation_QR_2026-10-27/BUS230Assessment2Class2Group4_2026-10-27_QR.pptx';data['previous_source_sha256']='0890d46b98bbca6b47205e41789edf3a06f44ada8fdfa1e2eb745ba2ae31e0d0'
for item in data['slides'][18:]:
 n=str(item['number']);tail=original[n].split('\nSOURCES\n',1)[1];notes[n]=f"Aram / Slide {n} / Planned {item['planned_seconds']} seconds\n\nSAY THIS\n{item['speech']}\n\nPRESENTER CUES\n{item['planned_window']}. {item['presenter_cues']}\n\nSOURCES\n"+tail
(r/'build/Script_Content_EN.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n');(r/'build/Aram_Notes.json').write_text(json.dumps(notes,ensure_ascii=False,indent=2)+'\n')
header='BUS230 ASSESSMENT 2 / CLASS 2 GROUP 4\nUPDATED FOR THE ALEX DEMONSTRATION / 27 OCTOBER 2026\n\nRead the English paragraphs aloud. Square brackets are presenter directions, not spoken words.\nThe 36-second demonstration starts automatically on slide 25 in Slide Show mode.\nSlides 1–18 and the other speakers’ words remain unchanged.\nPlanned timing only: rehearse with the actual projector. Q&A ends at 29:30, leaving 30 seconds.\n\n'
for name,items in [('BUS230_A2_Aram_Speaking_Text_EN_ALEX.txt',data['slides'][18:]),('BUS230_A2_Team_Speaking_Script_EN_ALEX.txt',data['slides'])]:
 chunks=[header]
 for it in items:chunks.append(f"SLIDE {it['number']} / {it['presenter'].upper()} / {it['title']}"+(f" / {it['planned_window']}" if 'planned_window'in it else '')+'\n\n'+it['speech']+'\n\n')
 (r/'output'/name).write_text('\n'.join(chunks))
