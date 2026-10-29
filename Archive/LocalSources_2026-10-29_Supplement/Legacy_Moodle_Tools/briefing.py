#!/usr/bin/env python3
"""Собрать все дедлайны Murdoch (задания + квизы/экзамены + события) → отчёт на Рабочий стол."""
import os, sys, time, datetime, html, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import moodle

def norm(s):
    if not s: return ""
    x = html.unescape(s).strip()
    x = re.sub(r'\s*\(Due[^)]*\)', '', x); x = re.sub(r'\s+is due\s*$', '', x)
    return re.sub(r'\s+', ' ', x).strip()

def safe(fn, *a, **k):                                 # неактивный web-service не должен ронять весь отчёт
    try: return fn(*a, **k)
    except Exception as e: print(f"[warn] {e}", file=sys.stderr); return None

now = int(time.time()); items = []
courses = moodle.call("core_enrol_get_users_courses", userid=moodle.USERID) or []
cmap = {str(c["id"]): c.get("shortname", str(c["id"])) for c in courses}

asg = safe(moodle.call, "mod_assign_get_assignments")
for c in (asg or {}).get("courses", []):
    for a in c.get("assignments", []):
        if a.get("duedate") and int(a["duedate"]) >= now:
            items.append((int(a["duedate"]), c["shortname"], "Задание", norm(a["name"])))

if courses:
    qp = {f"courseids[{i}]": c["id"] for i, c in enumerate(courses)}
    qz = safe(moodle.call, "mod_quiz_get_quizzes_by_courses", params=qp)
    for q in (qz or {}).get("quizzes", []):
        if q.get("timeclose") and int(q["timeclose"]) >= now:
            items.append((int(q["timeclose"]), cmap.get(str(q["course"]), str(q["course"])), "Квиз/экзамен", norm(q["name"])))

ev = safe(moodle.call, "core_calendar_get_action_events_by_timesort", timesortfrom=now, limitnum=50)
for e in (ev or {}).get("events", []):
    items.append((int(e["timesort"]), (e.get("course") or {}).get("shortname", ""), "Событие", norm(e["name"])))

rank = {"Задание": 0, "Квиз/экзамен": 0, "Событие": 1}; best = {}
for it in items:                                       # дедуп: одно событие в один день из разных источников
    when, course, kind, name = it
    key = f"{course}|{name}|{datetime.datetime.fromtimestamp(when):%Y%m%d}"
    if key not in best or rank[kind] < rank[best[key][2]]: best[key] = it

lines = [f"ДЕДЛАЙНЫ MURDOCH — обновлено {datetime.datetime.now():%d.%m.%Y %H:%M} (время Дубая, UTC+4)",
         "⚠ Времена — в ВАШЕМ дубайском времени. В Moodle те же дедлайны показаны во времени Перта (+4 ч впереди).",
         "=" * 64]
urgent = []
for when, course, kind, name in sorted(best.values()):
    dt = datetime.datetime.fromtimestamp(when); days = (dt - datetime.datetime.now()).days
    flag = "!!! " if days <= 1 else "!!  " if days <= 3 else "!   " if days <= 7 else "    "
    lines.append(f"{flag}{dt:%d.%m %H:%M}  ({days:2} дн.)  [{course}]  {kind}: {name}")
    if days <= 3: urgent.append(f"• {dt:%d.%m %H:%M} ({days} дн.) [{course}] {name}")

report = "\n".join(lines)
_here = os.path.dirname(os.path.abspath(__file__))
open(os.path.join(_here, "deadlines.txt"), "w").write(report)          # всегда: папка проекта (не TCC-защищена)
try:                                                                    # Desktop — по возможности (launchd под TCC не сможет)
    open(os.path.join(os.path.expanduser("~"), "Desktop", "Дедлайны Murdoch.txt"), "w").write(report)
except Exception:
    pass
print(report)
if urgent: print("\n<<URGENT>>\n" + "\n".join(urgent))
