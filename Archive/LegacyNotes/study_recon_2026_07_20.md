---
name: study-recon-2026-07-20
description: "Разведка учебного фронта 20 июля 2026 — Moodle sweep: 23.07 = Debate 6,7,8 (НЕ Final Sprint), A3 требует PDF, свежие оценки"
metadata: 
  node_type: memory
  type: project
  originSessionId: d36992b7-ee35-42cd-9d05-b2d89580a608
  modified: 2026-07-20T13:17:34.026Z
---

> ⚠️ **АРХИВ ТРИМЕСТРА TMD 2026 — закрыт успешно.** Все четыре юнита сданы и оценены (итог зафиксирован 15.09.2026):
> BUS279 **78 / D** · BUS293 **80 / HD** · BUS363 **70 / D** · MSP200 **67 / C** — все `COMPLETED`, 12 CP, ни одного fail.
> Финальные цифры: [[tmd_2026_final_results]]. Текущий триместр — **TSD 2026, старт 24.08.2026**: [[tsd_2026_enrollment]].
> Всё ниже — история закрытого триместра, не текущее состояние.

# Разведка учёбы 20 июля 2026 (read-only Moodle sweep)
🔗 [[MEMORY]] · [[murdoch_moodle_api]] · [[msp200_a3_strategy]] · [[karen_grade_tracker]] · [[karen_study_base]]

Токен Moodle жив, `deadlines.txt` перегенерён 20.07 15:31 (был 12.07).

## 🔴 Поправка вольта №1 — «Final Sprint 23.07» БЫЛО НЕВЕРНО
- **23.07 19:59 (Дубай) = `Debate submission: debate 6,7,8`, Word .docx**, cutoff (late) до **31.07 19:59**, 1 попытка,
  фильтр типов `.docx,.doc`. НЕ СДАНО. Это Assessment 1 (AI Debate, 8×2.5% = 20%; блок 6-8 = 7.5%).
- **Final Sprint = Sprint 4, Lesson 12, ОФЛАЙН в классе, портала сдачи в Moodle НЕТ и дедлайна нет.**
  TO DO к нему (из курса): знать Website Architecture · Creative Storyboarding · Channel Strategy · Ad Spend ·
  Target Market · AIDA · Competitive advantage · General Strategy. Даты уроков 11/12 в Moodle НЕ опубликованы.
- Спринты 1-3 сданы (18.06 / 02.07 / 16.07); Sprint 3 **submitted 16.07**, оценки пока нет.
- Механика дебатов: NotebookLM-чат → скопировать ВЕСЬ чат в Word → имя файла `35553299 Debate 6,7,8`.
  Свои примеры обязательны (без них низкая оценка); грейдится самим NotebookLM.
  Ссылки: Debate 6 = notebook/b65b53a0-339e-4918-95f6-07d2374fc482 · Debate 7 = dc7bad1c-6a92-442c-aa50-0fc67ebbbf9b ·
  Debate 8 = 6063e8db-1703-42fe-8063-419ccec5aa6c
- Quiz 3 — Lesson 11, даты в Moodle нет.

## 🔴 Поправка вольта №2 — MSP200 A3 просит PDF, а документы .docx
Intro задания: **Document type: PDF · Cover sheet: Yes (Name/Student ID/Unit Code/Assessment number and title) ·
APA 7 или Chicago · вес 30% · word minimum: various.** Портал принимает любые типы (фильтр пуст) + online text,
но требование в тексте — PDF. Инструкции и рубрика A3 не менялись с 21.05 → содержание готовых работ актуально.

## Оценки на 20.07 (новое против [[karen_grade_tracker]])
- BUS279: Debate 1-3 = 85 · Quiz 1 = 95 · **Quiz 2 = 95** (форум 20.07) · **Presentation 1 = 72** ·
  **Presentation 2 = 73** · **Sprint 1 = 75** (Distinction «The Practitioner»). Debate 4,5 и Sprint 3 — сданы, без оценок.
- BUS293: **Team Report = 69.70** · квизы 1-5 = 90/100/90/100/95 (итого 14.25/15 = 95%) · Reflection Video сдан 15.07, без оценки.
- BUS363: **Assessment 1 = 13.5/20 (67.5%)** · A2 (Project Plan) сдан 04.07, без оценки.
- MSP200: **A1 = 70.95 · A2 = 69.88** (журнал закрыт `nopermissiontoviewgrades`, взято из submission-status).
- Повторяющийся фидбек BUS279 (обе презентации): не читать со скрипта, показывать документ на экране,
  спонтанная подача, голос/язык тела. Учесть в будущих устных.

## ✅ Дебаты 6,7,8 ПРОЙДЕНЫ 20.07 — файл к сдаче собран
Все три чата NotebookLM пройдены за один вечер, Сэр вёл, я давал реплики ход за ходом.
Лежит в `Murdoch/К сдаче/BUS279 Debates 6,7,8 (23 июля)/`:
`35553299 Debate 6,7,8.docx` (~9800 слов, титул + 3 раздела) + три `debateN-...-raw.md` с расшифровками.
- Debate 6 (Lesson 9, Advanced Data): кейс Soundcore/Noon, postcode-фрикция, Clarity vs Hotjar, ветка про CLV и дискаунт-отравление данных.
- Debate 7 (Lesson 10, Strategic Fortress): Careem/Talabat, X vs птичка, кофейня за 22 dh, «рецепт» для доски и Stories.
- Debate 8 (Lesson 11, Biological Risk Architecture): MacBook как Cortisol-риск, авто-пауза абонемента, loyalty penalty страховщиков, IKEA-эффект в подписке на обжарку.
**Приём, который сработал:** держать сквозной сюжет (кофейня/Soundcore) через все три + в каждом дебате 2-3 раза спорить с источником и один раз честно уступить очко. AI закрыл все три хвалебными итогами.
**Сэру осталось:** загрузить .docx в портал (только .docx/.doc, 1 попытка, дедлайн 23.07 19:59, late до 31.07).

## Новое за 12-20.07
- BUS293: анонс 12.07 «Assessment 2 marks released».
- BUS279: форум 20.07 «Quiz 2 Marks». Иных анонсов по Final Sprint/Lesson 12 НЕТ.
- Дедлайны BUS363 (01.08 / 02.08 / 09.08 / 17.08) и MSP200 24.07 — без изменений с 12.07.
