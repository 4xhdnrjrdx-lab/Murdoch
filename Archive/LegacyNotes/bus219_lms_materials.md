---
name: bus219-lms-materials
description: "BUS219 — полная выгрузка LMS от 15.09.2026: карта курса (20 секций), 34 скачанных файла в Murdoch/BUS219/, кейсы и чтения по 12 темам, объявление лектора, состояние журнала"
metadata:
  node_type: memory
  type: project
  source: "Moodle courseid 31585, read-only GET 15.09.2026"
  modified: 2026-09-15
---

# BUS219 — выгрузка LMS (15.09.2026)
🔗 [[bus219_unit_outline]] · [[tsd_2026_enrollment]] · [[murdoch_moodle_api]]

Курс `BUS219tsd_26`, **courseid 31585**. Снято read-only, ничего не менялось и не сдавалось.
Файлы лежат в **`~/Documents/Murdoch/BUS219/`**, разложены по папкам вида `<№ секции> <Название>`.
Сырые JSON-ответы Moodle — в `BUS219/_lms_dump_2026-09-15/`.

**Скачано 34 файла (~15 МБ). Unit Outline из LMS НЕ скачивался** — по прямому запрету Сэра;
его содержание зафиксировано отдельно из присланного файла: [[bus219_unit_outline]].

## Структура курса: 20 секций
Видимых студенту — 16. **Скрыты четыре:** `Final Exam - TJD 2026`, `Migrated Quiz`,
`Supplementary Exam - TJ 2021`, `BUS219 Final Exam TMD 2023` — это остатки прошлых наборов,
содержимое не отдаётся (`uservisible = false`).

- **[0] Unit information** — Communication Board · форум Announcements · Main Discussion Forum
  (пуст) · приватный канал `dialogue` к Dr David Zhang · подсекция Teams Online Classes ·
  ресурс Unit Outline TSD 2026 *(не трогал)*.
- **[2] Assessments** — единственный модуль: папка **«Assignment guidelines, forms and marking guides»**
  (6 файлов, все скачаны). **Порталов сдачи нет ни одного.**
- **[3] Academic Integrity** — Academic Integrity Slide deck 3.pptx · Exam protocols.pptx.
- **[4]–[15] Topic 1…Topic 12** — по одинаковому шаблону: Pre-workshop (слайды + запись лекции) →
  Workshop (кейс для разбора) → Post-workshop (рекомендованное чтение + вопросы главы).
- **[19] Teams Online Classes** — гайд по подключению + два модуля `teammeeting`
  «BUS219 Teams Online Class 1 / 2 — Navneet Walia».

## Что скачано (по папкам `Murdoch/BUS219/`)
- **`02 Assessments/`** (6): `BUS219 Project Proposal marking guide.doc` ·
  `BUS219 Major Project Report marking guide.doc` · `Policy on Group Projects.doc` ·
  `Group Charter.doc` · `Major Project Peer Evaluation.doc` ·
  `Group Project team meeting time sheet.doc`. **Это рабочий комплект для командного проекта** —
  структура отчёта и критерии оценки лежат именно в marking guides.
- **`03 Academic Integrity/`** (2): слайды по академической честности и **протоколы экзамена**.
- **`04`–`15 Topic 1…12/`** (25): лекционные слайды по каждой сессии (`SessionN chapterNN.pptx`),
  кейсы воркшопов в PDF, плюс дополнительные колоды: мировые экономики (сессия 3), оценка
  политических рисков (сессия 5), формирование стратегии и типы контроля (сессия 8),
  доп. кейс про Польшу (сессия 4).
- **`19 Teams Online Classes/`** (1): `Student Guide - Joining Teams Online Sessions.pdf`.

**Чего в файлах нет:** записи лекций — это модули `alplinks` (12 штук, по одной на сессию),
внешние ссылки на плеер, файлом не выгружаются. Открывать по ссылке:
`moodleprod.murdoch.edu.au/mod/alplinks/view.php?id=…` (id 3111397, 3111407, 3111416, 3111425,
3111437, 3111447, 3111456, 3111466, 3111474, 3111483, 3111491, 3111500 — по порядку сессий 1…12).

## Кейсы воркшопов и чтения по темам (всё со ссылками на страницы Gaspar)
| Тема | Кейс воркшопа | Рекомендованное чтение |
|---|---|---|
| 1. Rise of Globalisation | Asia: Reducing Export Dependency (pp9) | Biofuels: Sustainable Development & Energy Security (pp29) |
| 2. Evolution of IB | Economic nationalism (pp54) | Predatory Trade Practices: Game of Chicken (pp49) · Stabilising Sierra Leone's Economy (pp52) |
| 3. Integration & Exchange Rates | Is the Chinese Renminbi Undervalued? (pp98) | Iceland's Economic Woes (pp111) · The EU Sans Frontière? (pp85) |
| 4. Cultural Environment | Advertising Clients about Cultural Aspects of Exporting to Ecuador (pp138) | Recognition of Values and Attitudes (pp121) · Right or Wrong? It Depends on the Culture (pp132) |
| 5. Legal & Political | Влияние политики «одного ребёнка» в Китае (pp147) | Becoming a King? (pp163) |
| 6. Corruption & Ethics | Walmart's Environmental Stewardship (pp175) | ExxonMobil: Why Are Corporate Ethics Codes So Important? (pp188) |
| 7. Entry Strategies | Medical Tourism (pp200) | Too Big to Fail? (pp211) |
| 8. Control of Global Business | McDonald's Liability for its U.S. Franchisees (pp232) | Berkshire Hathaway's Investment Strategy (pp236) |
| 9. Organisation of Global Business | Inflated Figures | Best Organisational Structure for Royal Dutch/Shell (pp258) |
| 10. International HRM & Marketing | Expatriates in Qatar (pp277) | Marketing Equine-related Products (pp311) |
| 11. Operations & Supply Chain | Outsourcing Production of Televisions (pp323) | Supply-Chain Disruptions (pp331) · When Is an American Car Really American? (pp334) |
| 12. Finance, Accounting, Taxation | Executive Compensation Rules in Financial Institutions (pp353) + **Exam preparation** | вопросы в конце главы |

В каждой теме post-workshop дополнительно требует «пройти Chapter Questions в конце главы».

## Объявления
Форум Announcements — **ровно один пост** за весь триместр:
**09.09.2026, Dr Navneet Walia, «Group Formation & Pre-Workshop Reminder»**:
1. **Сформировать группы по 4 человека** для презентаций на Week 6 и **прислать лектору имена по email.**
2. Ссылка на отчёт McKinsey «Geopolitics and the Geometry of Global Trade: 2026 Update»
   (`mckinsey.com/mgi/our-research/geopolitics-and-the-geometry-of-global-trade-2026-update`),
   обсуждался в классе 08.09.
3. Просьба смотреть слайды и запись ДО следующей лекции.

Main Discussion Forum пуст — ни одной темы.

## Состояние журнала (gradereport)
Журнал BUS219 доступен, но **заполнен мусором от прошлых наборов**: строки `Final Exam` (max **40**),
`exam mark` (max 100), `Participation (10) A`, `Total`, плюс три технические строки
`Lecture recording Session 2/3/5` (модули `alplinks` с max 100). **Оценок нет ни одной, весов нет,
строк под квизы и командный отчёт ещё не заведено.** То есть журнал под TSD 2026 преподаватель
пока не пересобрал — сверять веса с Unit Outline сейчас не с чем.

## Порталы сдачи
**В курсе нет ни одного `assign` и ни одного `quiz`.** Сдавать физически пока некуда:
квизы (Week 8/10 и 14) и портал под Major Project Report ещё не открыты. Календарных событий
у BUS219 тоже нет — в отличие от BUS225/BUS230/BUS334. Проверять повторно ближе к Week 6.

## Текстовый слой курса — вынесен в файлы (15.09.2026)
Помимо скачанных вложений, из Moodle снят **текст самого курса**, которого нет ни в одном файле:
- **`BUS219/00_СТРУКТУРА_КУРСА.md`** — все 20 секций по порядку: описания тем (learning outcomes,
  essential + recommended readings с указанием страниц Gaspar), 62 надписи-инструкции (`label`)
  из блоков Pre-workshop / Workshop / Post-workshop, ссылки на 12 записей лекций (`alplinks`),
  два Teams-класса и приватный канал к координатору. Это и есть «что делать по каждой сессии».
- **`BUS219/01_ОБЪЯВЛЕНИЯ.md`** — форумы: единственный пост от 09.09.2026 целиком (Group Formation
  & Pre-Workshop Reminder), Main Discussion Forum пуст.
- **`BUS219/00_UNIT_OUTLINE_BUS219_TSD2026.md`** — копия Unit Outline, присланного Сэром
  (не из LMS), положена рядом с материалами для удобства; разбор — в [[bus219_unit_outline]].
