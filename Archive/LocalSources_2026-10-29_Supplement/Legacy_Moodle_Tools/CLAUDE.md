# Murdoch Moodle — доступ и тьютор (для Claude)

Пользователь — **Faiaz Dzhafarov** (Murdoch Dubai, studentId 35553299, Moodle userid 257560). Зови «Сэр».
Настроено 12 июля 2026. ОС — macOS (UTC+4). Реализация — Python (macOS-ветка runbook).

## Файлы (в `~/murdoch-moodle/`)
- `.moodle_token` — web-service токен (chmod 600, В ЧАТ НЕ ВЫВОДИТЬ, в git не коммитить).
- `moodle.py` — обёртка API (`moodle.call(fn, params=None, **kw)`, `moodle.get_file(url, out)`, `moodle.USERID`).
- `briefing.py` — все дедлайны → `deadlines.txt` (в проекте) + Рабочий стол (по возможности). Рендер в ЛОКАЛЬНОМ времени (UTC+4).
- `notify.sh` — утренний попап (osascript) при дедлайне ≤3 дней. Запускается launchd в 08:00.
- `ACCESS.env` — параметры (userid, срок токена, таймзоны).

## Как пользоваться (примеры)
```bash
cd ~/murdoch-moodle
/usr/bin/python3 -c "import moodle; print(moodle.call('core_webservice_get_site_info')['fullname'])"
/usr/bin/python3 briefing.py                      # дедлайны
```
Курсы: `core_enrol_get_users_courses userid=USERID`. Задания: `mod_assign_get_assignments`.
Квизы: `mod_quiz_get_quizzes_by_courses` (courseids[0..]). Материалы курса: `core_course_get_contents courseid=..`.

## Обновление токена (истёк / «invalidtoken»)
Токен добывается ТОЛЬКО из SSO-сессии в браузере (локального пароля нет):
1. Пользователь залогинен в `https://moodleprod.murdoch.edu.au/my/` в Chrome.
2. Открыть DevTools → Network → включить Preserve log.
3. В адресе: `.../admin/tool/mobile/launch.php?service=moodle_mobile_app&passport=112233&urlscheme=moodlemobile`
4. У запроса `launch.php` → Response Headers → `Location: moodlemobile://token=<BASE64>`.
5. base64 → декод → среднее поле `:::` = токен (32 hex) → в `.moodle_token`.
   ⚠ Извлекать через Claude-for-Chrome НЕ вышло: расширение НЕ логирует кастомную схему `moodlemobile://`
   (нет в network-log, JS не читает 303-редирект, вкладка держит URL доли секунды). Надёжно — DevTools вручную.

## Известные грабли (macOS)
- **launchd + TCC**: агент НЕ пишет в `~/Desktop`/`~/Documents` (PermissionError) → `briefing.py` пишет в
  `~/murdoch-moodle/deadlines.txt` (не под TCC); Desktop — в try/except (работает при ручном запуске).
- **Таймзона**: Мак UTC+4, Moodle показывает Перт (UTC+8). briefing рендерит ЛОКАЛЬНО (+04) с явной меткой.
  Дедлайн, что в Moodle 13:00, у пользователя наступает 09:00.
- Токен: в чат не выводить; папку держать вне iCloud (Desktop/Documents синкаются) — она в `~` (ок).
- Первый попап launchd может запросить разрешение Automation/Уведомления — норм.

## Статус
✅ LIVE (12 июл 2026): токен валиден, API 458 функций, 8 курсов, briefing+launchd работают. Токен до 4 окт 2026.
