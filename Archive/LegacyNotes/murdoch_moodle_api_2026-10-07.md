---
name: murdoch-moodle-api
description: "Прямой доступ к Moodle Murdoch через web-service API + напоминалка дедлайнов (launchd 08:00), настроено на Маке"
metadata: 
  node_type: memory
  type: reference
  originSessionId: 2446fad7-9482-4f83-96fa-7424aad5bdc3
---

# Murdoch Moodle API — прямой доступ (LIVE с 12 июля 2026)
🔗 [[MEMORY]] · [[feedback_mac_launchd_documents]] · [[jarvis_git_repo]] · [[karen_study_base]]

## Актуальное состояние доступа — 7 октября 2026

- Пользователь подтвердил вход через Microsoft Authenticator. Новый токен получен штатным мобильным входом Moodle через Chrome и установлен в существующий файл `/Users/king1/murdoch-moodle/.moodle_token` с правами `600`.
- Проверены `core_webservice_get_site_info` и `core_enrol_get_users_courses`: учётная запись userid 257560; доступны текущие BUS219, BUS225, BUS230 и BUS334. Затем отдельно проверено, что существующий `moodle.py` работает с сохранённым токеном.
- Значение токена не хранится в этой заметке и не предназначено для GitHub. Временный HAR удалён, сетевой журнал очищен.
- Точный срок действия нового токена не установлен. Дата «до ~4 октября 2026» ниже относится к прежнему токену и сохраняется только как история.
- Это обновление доступа; фоновые проверки, отправки работ и сообщения не выполнялись. Общее восстановление через GitHub и независимое от Mac хранение секрета ещё нужно настроить в задаче создания базы Murdoch.


Настроен **прямой доступ к Moodle Мёрдока через web-service REST API** на Маке — в дополнение к вольту Карен
(тот кормится с почты; этот тянет курсы/дедлайны/материалы/рубрики напрямую). Всё в `~/murdoch-moodle/`.

## Что есть
- **Токен** `~/murdoch-moodle/.moodle_token` (chmod 600, userid 257560, сервис «Moodle mobile web service»,
  действует **до ~4 окт 2026**). В ЧАТ НЕ ВЫВОДИТЬ, в git не коммитить.
- `moodle.py` (обёртка: `call/get_file/USERID`), `briefing.py` (дедлайны→`deadlines.txt`+Desktop),
  `notify.sh` (osascript-попап), `ACCESS.env`, `CLAUDE.md`, `README.md`.
- **launchd** `com.murdoch.deadline` — ежедневно **08:00** попап при дедлайне ≤3 дней.
- API живой: 458 функций, 8 курсов, скачивание материалов (PDF) работает.

## Как добывался токен (важный урок)
SSO-only (нет локального пароля) → токен только из `admin/tool/mobile/launch.php?...&urlscheme=moodlemobile`.
**Claude-for-Chrome НЕ смог его вытащить**: расширение не логирует кастомную схему `moodlemobile://` в
network-log; JS не читает 303-редирект (fetch → «Failed to fetch»); вкладка держит `moodlemobile://token=`
доли секунды и сбрасывается; managetoken.php показывает только ИМЯ токена, не значение; страница «Security keys»
таблица «Key» = ключ КАЛЕНДАРЯ (не ws-токен, отсюда первый «invalidtoken»). **Рабочий путь: DevTools вручную** —
Network → launch.php → Response Headers → `Location: moodlemobile://token=<base64>` → декод (среднее поле `:::`).
Обновление токена — так же (в `CLAUDE.md` проекта пошагово). Сэр разрешил разовую экспозицию токена.

## Грабли (уже обойдены в коде)
- **launchd+TCC**: агент не пишет `~/Desktop`/`~/Documents` (PermissionError) → пишем в `deadlines.txt` в проекте,
  Desktop — try/except. (Тот же урок, что [[feedback_mac_launchd_documents]].)
- **Таймзона**: Мак UTC+4, Moodle показывает Перт (UTC+8). briefing рендерит ЛОКАЛЬНО с меткой. Дедлайн, что в
  Moodle 13:00, у Сэра наступает 09:00.

## ⚠️ Мак-попап УДАЛЁН (12 июл) — фрагильно
launchd `com.murdoch.deadline` **снесён** (bootout + plist удалён): Мак бывает выключен/крышка закрыта/Сэр
спит в 8 утра. Скрипты (`moodle.py`/`briefing.py`/токен) ОСТАЛИСЬ — переиспользует Карен.

## 🎯 NEXT (свежая сессия, чистый контекст): интегрировать Moodle-дедлайны в КАРЕН → Telegram
Цель: Карен сама тянет дедлайны из Moodle API и **шлёт напоминания в Telegram** (не попап на Маке).
Надёжно когда Мак вкл; станет always-on после переезда Jarvis/Karen на Linux.
- **Что есть в Карен уже:** `jarvis/deadlines.py` (+`bot._try_fast_deadlines` «какие дедлайны» on-demand),
  `jarvis/reminders.py` (плановая доставка в Telegram, `reminders.start_thread`), email-ingest дедлайнов в вольт.
- **Подход:** добавить Moodle-клиент в `jarvis/` (перенести логику `~/murdoch-moodle/moodle.py`, токен → в config/секреты),
  фоновый job: раз в день дайджест + нуджи за N дней до дедлайна, время **Дубай UTC+4** (Moodle=Перт UTC+8, +4ч).
  Переиспользовать доставку из `reminders.py`; гейт как у worksend (учебный профиль=Карен).
- **Решить с Сэром:** во сколько дайджест; нуджи за сколько дней; какие курсы; формат сообщения.
- **Токен:** `~/murdoch-moodle/.moodle_token`, до ~4 окт 2026; рефреш — DevTools вручную (см. проект `CLAUDE.md`).
- **Chrome-вкладка НЕ нужна** для доступа: API работает по сохранённому токену; браузер только для рефреша токена.
- Правки Карен = через git PR ([[jarvis_git_repo]]); тесты standalone `python3 tests/test_*.py`; рестарт `restart-safe.sh karen --yes`.

## Заготовка runbook для других студентов
`~/Downloads/MURDOCH-CLAUDE-SETUP.md` — обобщённая инструкция (Windows+macOS ветки), я её усилил 12 июл:
безопасный декод токена, полная macOS-ветка (Python+launchd), грабли TCC/iCloud. См. также [[karen_study_base]].
