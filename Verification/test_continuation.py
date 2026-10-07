#!/usr/bin/env python3
"""Acceptance check using only records in this checkout, without prior chat or source Mac."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
registry=json.loads((ROOT/'COURSES.yaml').read_text());courses={c['code']:c for c in registry['courses']}
def task(code,id):
 tasks=json.loads((ROOT/courses[code]['path']/'TASKS.json').read_text())['tasks']
 return next(t for t in tasks if t['id']==id)
assert len(courses)==8
assert all(courses[c]['status']=='успешно завершён' for c in ['BUS279','BUS293','BUS363','MSP200'])
assert [courses[c]['result']['mark'] for c in ['BUS279','BUS293','BUS363','MSP200']]==[78,80,70,67]
assert task('BUS225','A1')['status']=='сдано' and task('BUS225','A1')['correction']
assert task('BUS230','A1')['status']=='оценено' and any(e['date']=='2026-10-05' for e in task('BUS230','A1')['evidence'])
assert task('BUS334','A2')['status']=='оценено'
assert task('BUS219','A2')['status']=='согласовано'
assert task('BUS334','A2')['grade']['value']==15 and task('BUS334','A2')['grade']['maximum']==20
assert 'пять' in (ROOT/'BUS219/2026-TSD/TEAM.md').read_text().lower()
assert 'Class 2 Group 4' in (ROOT/'BUS230/2026-TSD/TEAM.md').read_text()
assert (ROOT/'BUS225/2026-TSD/Assignments/A1/Video/BUS225_A1_Faiaz_Dzhafarov.webm').stat().st_size==73538655
assert json.loads((ROOT/'ACCESS_STATUS.json').read_text())['lms']['result']=='ok'
assert (ROOT/'RESTORE.md').is_file() and (ROOT/'AGENTS.md').is_file()
print('PASS: eight courses, official completed results, submitted work and separate correction, group evidence, full video, access limit and next-chat instructions recovered solely from this checkout')
