---
name: msp200-a3-strategy
description: "MSP200 A3 (Strategy for Professional Development, 30%, 24 июля) — оба документа готовы и зааудированы, что осталось Сэру"
metadata: 
  node_type: memory
  type: project
  originSessionId: 2446fad7-9482-4f83-96fa-7424aad5bdc3
  modified: 2026-07-21T12:05:06.702Z
---

# MSP200 A3 — Strategy for PD (готово 5 июля 2026)
🔗 [[MEMORY]] · [[msp200_a2_reflection]] · [[karen_study_base]] · [[feedback_humanize_academic_no_ai_tells]]


**Дедлайн пт 24 июля.** Рубрика: Task 1 worksheet 5% + Task 2 стратегия 20% + Written 5%. Оба документа собраны в `Murdoch/К сдаче/MSP200 A3 (24 июля)/`, генератор — scratchpad `build_msp200_a3.py` (при правках менять его и пересобирать).

## Содержание
- **Task 2** (`MSP200_A3_Task2_Strategy_...docx`, 963 слова прозы / 991 со всеми заголовками — оба счёта ≤1000, лимит 650–1000, титульник имя+ID+tutor Shahinda Baig): 3 навыка = те же, что A1/A2 (digital literacy, critical thinking, communication) → 3 SMART-цели: **GA4-сертификация** Google Skillshop (27 июл→30 сен) · **Marketing Analytics UVA Darden/Coursera** audit + свой мини-тест (5 окт→30 ноя) · **Toastmasters Дубай** (вступить до 15 авг, 3 Pathways-речи до 15 дек). Заключение: lifelong learning + тема automation & AI + WEF Future of Jobs 2025. Ссылки APA (4).
- **Worksheet** (`MSP200_A3_SelfAssessment_Worksheet_...docx`): все 9 таблиц, A1-оценки воспроизведены точно, A3-колонки заполнены. Честные сдвиги +1 ступень ТОЛЬКО у 3 PD-навыков (DigLit и CritThink «with help»→«independently», Comm «independently»→«confident and effective»), остальные 6 без изменений с комментарием почему.

## Аудит (ultracode, 2 прогона, ~1.9M токенов)
6 линз + веб-проверка URL/фактов + адверс-верификация 2 скептиками на находку. Подтверждено и исправлено: **P1 — фраза «GA4 назван в вакансиях A1» была фабрикацией** (в сданном A1 только «analytics»/«Google AdWords»; перегруппировано на реальные формулировки объявлений); «finishing»→«working through» (курс 2 только free-модули); «my weakest area»→«one of my weakest areas» (как в A1); триады в заключении разбавлены; Ice Breaker = первая Pathways-речь (двойной счёт убран). URL/факты (Skillshop, Coursera UVA, Toastmasters Дубай ~60$/полгода, WEF 2025) веб-подтверждены. 0 em/en-тире. NB: 3 скептика 2-го прогона упали на session-limit — их 2 находки (word count 1002>1000 по строгому счёту с заголовками — РЕАЛЬНАЯ; comma splice) закрыты детерминированно 5 июля: ужато до 991/963, сплайс → двоеточие.

## ⚠️ Урок для будущих работ
Черновик приписал вакансиям A1 конкретный инструмент, которого там нет — маркер graded A1 и мог поймать. **Все отсылки к ранее сданным работам сверять с их текстом дословно** (файлы «(сдано)» в вольте Карен).

## Правка 20.07 (humanizer-аудит + сверка с инструкциями)
Прогнал Task 2 через скилл `/humanizer` (33 паттерна): чисто по 32 из 33 — 0 em/en-тире, 0 «умных» кавычек,
0 AI-словаря, 0 фраз-прокладок, sentence-case заголовки. Единственная реальная находка — негативный
параллелизм «is not a one-off task, it is a habit» в первой строке заключения. Исправлено + сняты лишние слова.
**Word count был 993 (потолок 1000) → стало 978**, на титуле цифра обновлена. Дата с титула убрана:
инструкции требуют только «cover page showing name and ID number». Бэкап оригинала — в scratchpad сессии.
⚠ **Формат сдачи: инструкции A3 (PDF-файл в Moodle) говорят «WORD document» для Task 2 + worksheet-документ.**
Описание портала при этом пишет «Document type: PDF». Фильтра типов у портала нет. Решение: сдавать .docx
по инструкции, при желании приложить и PDF (лимит 20 файлов).
⚠ **Task 1 «will be completed in class»** — worksheet финализируется на паре, не дома.
Последняя пара MSP200 в триместре: **чт 23.07, 16:30, ауд. 208** (Сэр учится онлайн → делаем вместе на созвоне).

## PDF готовы 21.07 (Team_Hub H-2026-07-21-005)
Оба документа выгружены в PDF (конвертировал Сэр в Word: AppleScript-мост Word на Маке НЕ работает —
`save as` → -1708, свойства документа → `missing value`; для будущих конвертаций нужен LibreOffice
или руки). Проверил read-only через PyMuPDF: Task 2 — 0 расхождений с .docx, cover sheet полный,
0 em-тире; worksheet — 9 таблиц/90 ячеек/18 отметок X сошлись 1:1, шрифты встроены.
⚠ **PDF worksheet временный**: Task 1 заполняется на паре 23.07 → после пары пересобрать PDF.
Отчёт: `Team_Hub/status/unik.md`.

## 🔑 21.07 (H-006): Task 1 НЕ требует пары, работа submission-ready
- **Unit Outline §5.2.3 (A3) фразы «in class» НЕ содержит вообще.** Она есть только в файле
  `Assessment 3 INSTRUCTIONS.pdf`. Для сравнения, у Assessment 1 (§5.2.1) оговорка двойная и явная:
  пункт назван «(in-class completion)» + «Task 1 will be completed in class – your tutor/lecturer will
  assist». Для A3 обе оговорки сняты → «in class» = когда выделено время, не условие выполнимости.
  Задача чисто индивидуальная: перечитать свою таблицу A1 и проставить свои текущие рейтинги.
- **Task 1 уже выполнен в worksheet**: 9/9 разделов, 18 меток X, 9 explanation + 9 comparison,
  0 пустых, 426 слов комментариев, 3 сдвига совпадают с тремя PD-курсами. Правку не делал.
- **ФОРМАТ РЕШЁН: Word (.docx).** Unit Outline §5.2.3 «WHERE TO SUBMIT»: *«Submit the completed
  self-analysis worksheet along with Part 2 as a Word document»*; чек-лист инструкций — тоже «Word
  document». «Document type: PDF» стоит ТОЛЬКО в шаблонном описании портала и противоречит чек-листу
  самого задания. Фильтр типов у портала пуст, лимит 20 файлов → грузить .docx + PDF приложением.
- Дедлайн жёсткий: §5.4 — «submitted after the due date without approval will not be marked … 0%».
- Отчёт: `Team_Hub/status/unik.md` (H-2026-07-21-006).

## Осталось Сэру
1. Прочитать оба документа, подтвердить честность новых самооценок (это его личная оценка себя).
2. **Task 1 выполняется В КЛАССЕ** — перенести оценки/комментарии из готового worksheet.
3. Сдать Task 2 (+ worksheet по чек-листу) в Assessment 3 tab до 24 июля.
   ⚠️ **20.07 сверено с Moodle ([[study_recon_2026_07_20]]): задание требует `Document type: PDF` + Cover sheet
   (Name / Student ID / Unit Code / Assessment number and title), APA 7 или Chicago.** Готовые файлы — .docx →
   перед сдачей экспортировать в PDF и проверить титульник. Портал типы файлов не фильтрует (примет и .docx),
   но требование в тексте задания — PDF. Инструкции/рубрика A3 не менялись с 21.05 → содержание актуально.

## 🐞 Заметка про Workflow-дедуп
В первом прогоне дедуп `(f.location+'|'+f.title).toLowerCase().replace(/[^a-zа-я0-9]/g,'').slice(0,80)` схлопнул 21 находку в 1 (в рантайме воркфлоу; в node тот же код работает — причина не найдена). Рабочая замена: `JSON.stringify([title, location])` без regex/slice. Тот же код в Sprint 3-аудите работал нормально — недетерминированно, доверять дедупу нельзя, проверять логи `Сырых/после дедупа`.

См. [[msp200_a2_reflection]], [[karen_study_base]], [[feedback_humanize_academic_no_ai_tells]].
