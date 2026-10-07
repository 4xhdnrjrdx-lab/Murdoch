---
name: tsd-2026-enrollment
description: "Триместр TSD 2026 — учёба началась 24.08.2026, зарегистрированы 4 юнита: BUS219, BUS225, BUS230, BUS334 (коды, названия, courseid)"
metadata:
  node_type: memory
  type: project
  modified: 2026-09-15
---

# TSD 2026 — текущий триместр (актуально на 15.09.2026)
🔗 [[tmd_2026_final_results]] · [[murdoch_moodle_api]] · [[karen_study_base]] · [[study_work_directives]]

**Учёба началась 24.08.2026** (в Moodle `startdate` всех четырёх курсов = 2026-08-24, Перт UTC+8).
Зарегистрированы **4 юнита**, все видимы в LMS:

| Код | Название юнита | shortname в Moodle | courseid |
|---|---|---|---|
| **BUS219** | International Business | `BUS219tsd_26` | 31585 |
| **BUS225** | Services Marketing | `BUS225tsd_26` | 31320 |
| **BUS230** | Change Management | `BUS230tsd_26` | 31305 |
| **BUS334** | Business Analytics | `BUS334tsd_26` | 31274 |

Источник: `core_enrol_get_users_courses` (live-GET 15.09.2026), userid 257560.
Предыдущий триместр TMD 2026 закрыт — итоги в [[tmd_2026_final_results]].

## Что сделано (обновлено 15.09.2026, вечер)
- **Unit Outline получены по всем четырём юнитам** — Сэр прислал файлами сам, из LMS не качались.
  Лежат в комнатах курсов как `00_UNIT_OUTLINE_<КОД>_TSD2026.md`. Разборы:
  [[bus219_unit_outline]] · [[bus225_unit]] · [[bus230_unit]] · [[bus334_unit]].
- **Все четыре курса выгружены из LMS**: BUS219 (34 файла) · BUS225 (49) · BUS230 (50) ·
  BUS334 (39). В каждой комнате: материалы по секциям, `00_СТРУКТУРА_КУРСА.md` (текстовый слой),
  `01_ОБЪЯВЛЕНИЯ.md`, сырые JSON в `_lms_dump_2026-09-15/`.
  Не качались: Unit Outline каждого курса (запрет) и 8 видеолекций BUS230 (229 МБ, есть транскрипты).
- Правило остаётся: **Unit Outline из LMS не скачивать никогда** — присылает Сэр.
## Что уже известно из живого Moodle (без Unit Outline, только календарь и порталы сдачи)
Снято 15.09.2026, read-only. Время дубайское (UTC+4); Moodle показывает Перт (UTC+8).
- **18.09 09:00** — BUS225 Service organisation profile (групповой портал, non-assessable,
  конец Session 4). Статус `new`, Сэру редактировать нельзя — сдаёт кто-то из группы.
- **18.09 19:59** — BUS230 **Assessment 1: Essay (Individual)**, портал 124982. **НЕ сдано.**
- **20.09 19:59** — BUS334 **Assignment 2: Questionnaire (20%)**, портал 124855. **НЕ сдано.**
- 02.10 17:00 — BUS225 Video Presentation (125039).
- 25.10 19:59 — BUS334 A3 Data Collection & Preliminary Analysis (30%) (124856).
- 06.11 17:00 — BUS225 Reflective Journal + Service Blueprint (групповой, 125040) и Peer review
  individual (125041); 06.11 19:59 — BUS230 Assessment 2: Presentation Material (Group) (124983).
- 19.11 13:00 — BUS334 Assignment 1: Engagement (10%) (124854). 28.11 — BUS334 Peer Evaluation (124858).
- BUS334 A4 Supporting materials: Data Analysis & Presentation (40%) — портал 124857, **срок не задан**.
- ⚠️ **У BUS219 в Moodle нет ни одного портала сдачи** (подтверждено выгрузкой 15.09) — только папка «Assignment guidelines, forms
  and marking guides» и «Exam Protocols». Оценивание либо ещё не открыто, либо идёт не через порталы.
- ⚠️ **В BUS225 Сэр ни разу не заходил** (`lastaccess = never`), а первый дедлайн у него ближайший.

## Доступ
Moodle API жив (`~/murdoch-moodle/`), режим read-only GET. **Токен действует до 04.10.2026** —
перевыпуск руками Сэра через Preferences → Security keys (SSO + MFA).

## Команды и групповые сдачи — состояние на 15.09.2026 (live)
Проверено `core_group_get_course_user_groups` + `mod_assign_get_submission_status`, read-only.

**Ни в одном из четырёх курсов Сэр не состоит ни в одной проектной команде.** Везде он числится
только в двух административных группах: `<КОД> Class 1|2` (поток) и
`SIS: <КОД>_ATTD_DUBAI-ISC_FACE TO FACE` (учёт очной посещаемости). Это не команды.

Последствия по групповым порталам:
| Курс | Портал | `submissiongroup` | Можно сдать? |
|---|---|---|---|
| BUS225 | Service organisation profile (125038, **18.09**) | `null`, groupid 0 | **нет** — `canedit=false`, `cansubmit=false`, `usergroups=[]` |
| BUS225 | Reflective Journal + Blueprint (125040, 06.11) | `null` | **нет**, та же причина |
| BUS230 | A2 Presentation Material (124983, 06.11) | `null` | **нет** — состоит в group’ах потока, но они не входят в grouping задания |
| BUS219 | — | — | портала вообще нет; команда живёт вне LMS |

**BUS219:** по Unit Outline команда собирается самостоятельно (4 человека, не больше), и **лидер шлёт
состав лектору по email** — в Moodle её и не должно быть видно. Срок по outline — сессия Week 4,
напоминание лектора было 09.09. Команда не собрана.

Вывод: пока Сэра не внесут в команду, три групповых портала для него физически закрыты. Это
вопрос к лекторам (BUS225 — первым, у него дедлайн 18.09), а не техническая проблема доступа.

### BUS225 — группа назначена (письмо лектора 15.09.2026, 19:35)
**Dana Khoury Eid** (лектор BUS225, в копии Cheryl Leo) разослала составы групп на **Assignment 2**
письмом «BUS225 GROUPS for Assignment 2» — кто не собрался сам, того распределили.

**Сэр — Group 9**, трое: `35553299 Faiaz D.` · `36090418 Muhammad Aun` · `36353092 Beky Sufyan`.
Всего 10 групп по 2–3 человека; Group 10 пустая. **Ретейлеры уже заняты: Group 1 — IKEA,
Group 2 — DECATHLON** (остальные не проставлены).

Что требует лектор **к 18.09**:
1. связаться с сокомандниками (письмо по student ID в поле «Кому»);
2. договориться о **ретейлере** для анализа;
3. заполнить приложенную форму (`Service organisation profile format`, .docx — есть и в LMS,
   секция Home) и **прислать ей по email** — не в портал Moodle.
Отдельно: **ретейлера она должна одобрить, до одобрения работу не начинать.** Детали Assignment 2
объяснит после сдачи Assignment 1.

⚠️ Расхождение: в Moodle тот же артефакт лежит порталом `Service organisation profile submission`
(125038) со сроком **18.09 09:00**, а в письме сказано слать почтой «by 18th September».
В Moodle группы на 15.09 всё ещё нет (`submissiongroup: null`, `cansubmit: false`) — то есть
портал для Сэра закрыт, работает только почтовый путь.

**BUS219 команды по-прежнему нет** — это другой предмет и другой лектор (Dr Navneet Walia),
письмо ей отправлено 15.09.
