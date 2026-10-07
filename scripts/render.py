#!/usr/bin/env python3
"""Render overviews from COURSES.yaml and per-course TASKS.json, then build manifest."""
from base import ROOT,COURSES,read,write,retained,digest
from urllib.parse import quote

def link(path,label):return f'[{label}]({quote(path,safe="/#")})'
for c in COURSES['courses']:
 path=c['path']; state=read(path+'/TASKS.json')
 lines=[f'# {c["code"]}: задания', '', '> Сформировано scripts/render.py из TASKS.json. Изменения статусов и сроков вносить в TASKS.json.', '', 'Все календарные сроки: Asia/Dubai (UTC+4). Неделя занятия без времени не превращается в точный дедлайн.', '', '| Работа | Состояние | Срок / проверка | Следующее действие |','|---|---|---|---|']
 for t in state['tasks']:
  due='; '.join(f'{x["value"]} (источник: {x["source_label"]}; проверено {x["checked_at"]})' for x in t.get('deadlines',[])) or 'Не установлен'
  lines.append(f'| [{t["id"]}: {t["title"]}](#{t["id"].lower()}) | {t["status"]} | {due} | {t["next_action"]} |')
 for t in state['tasks']:
  lines+=['',f'## {t["id"]}', '',t.get('detail',''), '', '**Основания:**']
  for e in t['evidence']:lines+=['',f'- {e["date"]}: {e["note"]} {link(e["path"],"Источник") if e.get("path") else e["source"]}']
  if t.get('grade'):
   g=t['grade'];lines+=['',f'**Оценка:** {g["value"]} / {g["maximum"]}, проверено {g["checked_at"]}. '+link(g['source_path'],'Источник')]
  if t.get('correction'):lines+=['', '**Исправление после сдачи:** '+t['correction']]
  if t.get('unknown'):lines+=['', '**Неизвестно:** '+t['unknown']]
 (ROOT/path/'TASKS.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
 rows=[]
 for t in state['tasks']:rows.append(f'- {link("TASKS.md#"+t["id"].lower(),t["id"]+": "+t["title"])}')
 (ROOT/path/'README.md').write_text(f'# {c["code"]} {c["name"]} | {c["period"]}\n\n'+ '\n'.join([link(x+'.md',label) for x,label in [('CONTEXT','Контекст и неизвестное'),('TASKS','Задания и следующие шаги'),('TEAM','Команда'),('HISTORY','История')]])+'\n\n'+link('Materials/README.md','Материалы преподавателя и упражнения')+'\n\n'+link('Assignments/README.md','Рабочие файлы, версии и подтверждения')+'\n\n'+link('Correspondence/README.md','Письма и уточнения')+'\n\n'+ '\n'.join(rows)+'\n\n'+link('../../README.md','Общая база')+'\n',encoding='utf-8')
access=read('ACCESS_STATUS.json')
lines=['# Murdoch: моя учёба','','Faiaz Dzhafarov · student ID 35553299 · время Asia/Dubai (UTC+4).','','Это приватная база: материалы, задания, решения и история сохраняются в GitHub. Для нового чата начните с [AGENTS.md](AGENTS.md). Для другого устройства: [RESTORE.md](RESTORE.md).','','## Сейчас','',]
for c in COURSES['courses']:
 if c['status']=='учимся':
  state=read(c['path']+'/TASKS.json')
  actions='; '.join(f'{t["id"]}: {t["next_action"]}' for t in state['tasks'] if t.get('show_on_overview'))
  lines += [f'### {link(c["path"]+"/README.md",c["code"])} · {c["status"]}', '']
  lines += [f'- {t["id"]}: {t["next_action"]}' for t in state['tasks'] if t.get('show_on_overview')]
  lines += ['']
lines+=['','Сроки, состояния отдельных работ и их основания доступны в таблицах заданий каждого предмета. Главная страница формируется из основных записей.','','## Завершённые предметы','','| Предмет | Итог по юниту | Период |','|---|---|---|']
for c in COURSES['courses']:
 if c['status']!='учимся':lines.append(f'| {link(c["path"]+"/README.md",c["code"])} | {c["status"]}: {c["result"]["mark"]} / {c["result"]["grade"]}, {c["result"]["credit_points"]} CP | {c["period"]} |')
lines+=['','Официальные итоги и источник хранятся в [COURSES.yaml](COURSES.yaml).','','## Свежесть и сохранение','',f'- Почта: проверена {access["mail"]["checked_at"]}. {access["mail"]["result"]}',f'- LMS: проверка {access["lms"]["checked_at"]}, результат `{access["lms"]["result"]}`. Даты и подтверждения по предметам приведены в заданиях.', '- GitHub: текущая опубликованная версия определяется SHA ветки main, показанным GitHub. Проверка локальной синхронизации: `python3 scripts/sync.py status`. Сверка файлов: `python3 scripts/verify.py`.', '- Проверки выполняются при начале работы по предмету или запросе статуса. Фоновых заданий нет.','','## Восстановление и открытые вопросы','','- [Результаты проверки восстановления](Verification/RESTORE_REPORT.md)', '- [Инвентаризация и перенос](Migration/README.md)', '- [Файлы и доступ, которые ещё нужно восстановить](Migration/GAPS.md)', '- [Подключение LMS и хранение токена](Access/Moodle/README.md)', '', 'Просмотр с iPhone: откройте репозиторий в Safari или GitHub и перейдите в нужный предмет. Документы скачиваются по ссылкам на файлы; для видео используйте Download raw file. Учётная запись GitHub и её восстановление должны быть доступны независимо от Mac. Полная копия создаётся по RESTORE.md.']
(ROOT/'README.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
files=[{'path':p.relative_to(ROOT).as_posix(),'bytes':p.stat().st_size,'sha256':digest(p),'storage':'git'} for p in retained()]
write('MANIFEST.json',{'schema_version':1,'hash':'SHA-256','scope':'All retained repository files except MANIFEST.json itself and .git internals. Self-hash would be recursive; Git commit verifies the manifest.','files':files,'file_count':len(files),'total_bytes':sum(x['bytes'] for x in files)})
print('Rendered overviews; manifest:',len(files),'files',sum(x['bytes'] for x in files),'bytes')
