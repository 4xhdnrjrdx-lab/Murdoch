# Murdoch Moodle → Claude: полная авто-настройка (инструкция для Claude)

**Ты — Claude в сессии студента Murdoch University.** Пользователь бросил тебе этот файл, чтобы ты
настроил ему полный доступ к его кабинету Moodle и сервис напоминаний/тьютора — так же, как это уже
сделано у другого студента. Действуй по этому файлу как по runbook: по шагам, с проверкой в конце.

> ВАЖНО про приватность: настраивай доступ **к аккаунту текущего пользователя**. В этом файле нет и не
> должно быть чужих токенов/логинов. Токен добывается из ЕГО собственной залогиненной сессии. Секреты
> (токен) **никогда не выводи в чат** — только записывай в файл на диск.

---

## 0. Что должно получиться (критерии «готово»)
1. Ты видишь все курсы пользователя, все дедлайны (задания + квизы/экзамены) с описаниями и все учебные материалы.
2. Настроено ежедневное напоминание о дедлайнах (всплывающее окно + файл на рабочем столе).
3. Ты можешь работать тьютором: находить и читать материалы курса и помогать с заданиями по реальным критериям.
4. Единственная точка «стоп» — вход в аккаунт: пароль/MFA вводит **сам пользователь**, ты пароли не вводишь.

## 1. Предпосылки (проверь и объясни пользователю по-человечески, без жаргона)
- **Claude Code** (десктоп) + расширение **Claude for Chrome**, подключённое к его Chrome.
- Пользователь **залогинен** в `https://moodleprod.murdoch.edu.au/my/` в этом Chrome.
- ОС: ниже — реализация для **Windows** (PowerShell + Планировщик задач). Если у пользователя **macOS/Linux** —
  логику работы с API (раздел 4) оставь идентичной, но замени загрузчик на `curl`, а напоминания — на
  `cron` + `osascript`/`notify-send`. Если сомневаешься в ОС — спроси одним вопросом.
- Университет тот же (Murdoch) → базовый URL один: `https://moodleprod.murdoch.edu.au`. Для другого вуза
  поменяй этот URL везде.

---

## 2. САМОЕ ГЛАВНОЕ И ХИТРОЕ: добыть API-токен из SSO-сессии

Вход в Murdoch — **только через Microsoft SSO + MFA**, локального пароля Moodle нет. Поэтому:

> ⛔ НЕ ПЫТАЙСЯ: `login/token.php` с логином/паролем — не сработает (нет локального пароля), а перебор
> ещё и грозит блокировкой аккаунта. Токен добывается ТОЛЬКО через мобильный launch-эндпоинт из браузерной сессии.

**Процедура (через инструменты Claude for Chrome):**

1. `list_connected_browsers` → выбери локальный → `select_browser`. Затем `tabs_context_mcp {createIfEmpty:true}` — получи tabId.
2. `navigate` вкладку на `https://moodleprod.murdoch.edu.au/my/`, затем `get_page_text`.
   - Если это Dashboard (видно курсы) — пользователь залогинен, продолжай.
   - Если редирект на `login.microsoftonline.com` — **попроси пользователя войти самому** в этом окне Chrome
     (логин + MFA). Пароль ты не вводишь. Дождись, повтори проверку.
3. `read_network_requests {clear:true}` — **вызови один раз, чтобы включить запись сети** (трекинг стартует с первого вызова).
4. `navigate` вкладку на launch-эндпоинт (passport — любое число):
   `https://moodleprod.murdoch.edu.au/admin/tool/mobile/launch.php?service=moodle_mobile_app&passport=482913&urlscheme=moodlemobile`
5. `read_network_requests` → найди запись, у которой **url начинается с `moodlemobile://token=`**. Скопируй всё
   после `token=` — это BASE64.
   - 🔑 Именно эта запись сети содержит токен и **не редактируется** расширением.
   - ⛔ НЕ трать время на обходные пути (я их проверил, не работают):
     - `fetch()`/JS в странице → кросс-схемный редирект даёт «Failed to fetch», токен не прочитать.
     - подмена `urlscheme` на свой URL → Moodle санирует параметр.
     - сама запись `launch.php` показывается как «pending» без заголовков — она не нужна, нужна отдельная `moodlemobile://…`.
6. **Сохрани токен, НЕ печатая base64 ни в ответе, ни как аргумент команды.** ⚠️ base64 — это САМ секрет
   (декодируется в токен); в аргументе командной строки он осядет в истории оболочки / транскрипте tool-call
   / логах. Правильный порядок:
   - **а)** файл-инструментом (Write), а НЕ `echo`/inline-аргументом, запиши строку base64 из сетевой записи
     во временный файл `<projdir>/.b64.tmp`;
   - **б)** декодируй из файла в `.moodle_token` (среднее поле `:::`), выставь права `600`, удали `.b64.tmp`.

   Windows (`<projdir>` = `C:\Projects\murdoch-moodle`):
   ```powershell
   $dir='C:\Projects\murdoch-moodle'; New-Item -ItemType Directory -Force -Path $dir | Out-Null
   $b64=(Get-Content -Raw "$dir\.b64.tmp").Trim()      # base64 уже в файле (положен Write-инструментом, не echo)
   $dec=[Text.Encoding]::ASCII.GetString([Convert]::FromBase64String($b64))
   $tok=($dec -split ':::')[1]          # формат: <md5hash>:::<ТОКЕН>[:::<priv>]  → среднее поле
   Set-Content -Path "$dir\.moodle_token" -Value $tok -NoNewline -Encoding ascii
   Remove-Item "$dir\.b64.tmp" -Force
   "token stored, length=$($tok.Length)"   # длина должна быть 32
   ```
   macOS/Linux — тот же принцип (base64 в файл, декод из файла); команда — в разделе **5м, шаг 1**.
7. **Проверь токен** (см. раздел 4, вызов `core_webservice_get_site_info`) — он вернёт имя и `userid` этого
   пользователя. Запомни их (нигде не хардкодь чужой userid).

---

## 3. Создай файлы-скрипты на диске (Windows-реализация)

> 🍎 **Если ОС = macOS/Linux — пропусти разделы 3–5 и иди в раздел «5м. macOS-ветка» (ниже).** Логика API
> там идентична, но реализация на Python (без jq/curl-массивов) + launchd/osascript.

> ⚠️ ГРАБЛИ КОДИРОВКИ: файлы `.ps1` с кириллицей сохраняй в **UTF-8 с BOM**, иначе Windows PowerShell 5.1
> ломает кириллицу и скрипт не парсится. После записи файла конвертируй:
> ```powershell
> $p='путь.ps1'; $c=Get-Content -Raw -Encoding UTF8 $p
> [IO.File]::WriteAllText($p,$c,(New-Object System.Text.UTF8Encoding($true)))
> ```

### Файл `moodle.ps1` (обёртка API; userid определяется сам)
```powershell
$script:MoodleBase  = 'https://moodleprod.murdoch.edu.au'
$script:MoodleToken = (Get-Content -Raw -Path (Join-Path $PSScriptRoot '.moodle_token')).Trim()

function Invoke-Moodle {
    param([Parameter(Mandatory=$true)][string]$Function,[hashtable]$Params=@{})
    $body=@{ wstoken=$script:MoodleToken; wsfunction=$Function; moodlewsrestformat='json' }
    foreach($k in $Params.Keys){ $body[$k]=$Params[$k] }
    $r=Invoke-RestMethod -Uri "$script:MoodleBase/webservice/rest/server.php" -Method Post -Body $body
    if($r -and $r.PSObject.Properties.Name -contains 'exception'){ throw "Moodle API error [$($r.errorcode)]: $($r.message)" }
    return $r
}
function Get-MoodleFile {
    param([Parameter(Mandatory=$true)][string]$FileUrl,[Parameter(Mandatory=$true)][string]$OutPath)
    [Net.ServicePointManager]::SecurityProtocol=[Net.SecurityProtocolType]::Tls12   # иначе "Unable to connect"
    $sep= if($FileUrl -match '\?'){'&'}else{'?'}
    $u="$FileUrl$sep`token=$script:MoodleToken"
    $wc=New-Object System.Net.WebClient                                             # WebClient берёт путь буквально (имена с []),
    try{ $wc.DownloadFile($u,$OutPath) } finally{ $wc.Dispose() }                   # Invoke-WebRequest -OutFile спотыкается о [ ] в имени
}
$script:MoodleUserId = (Invoke-Moodle 'core_webservice_get_site_info').userid       # свой userid, без хардкода
```

### Файл `briefing.ps1` (собирает все дедлайны → отчёт на рабочий стол)
```powershell
$ErrorActionPreference='Stop'
. (Join-Path $PSScriptRoot 'moodle.ps1')
function Dec($s){ if(-not $s){return ''}; ($s -replace '&amp;','&' -replace '&#39;',"'" -replace '&quot;','"' -replace '&nbsp;',' ').Trim() }
function Norm($s){ $x=Dec $s; $x=$x -replace '\s*\(Due[^)]*\)',''; $x=$x -replace '\s+is due\s*$',''; ($x -replace '\s+',' ').Trim() }
$now=[DateTimeOffset]::UtcNow.ToUnixTimeSeconds()
$items=New-Object System.Collections.Generic.List[object]
$courses=Invoke-Moodle 'core_enrol_get_users_courses' @{ userid=$script:MoodleUserId }
$cmap=@{}; foreach($c in $courses){ $cmap[[string]$c.id]=$c.shortname }
function CName($id){ if($cmap.ContainsKey([string]$id)){$cmap[[string]$id]}else{[string]$id} }
$asg=Invoke-Moodle 'mod_assign_get_assignments'
foreach($c in $asg.courses){ foreach($a in $c.assignments){ if($a.duedate -and [int64]$a.duedate -ge $now){
  $items.Add([pscustomobject]@{when=[int64]$a.duedate;course=$c.shortname;kind='Задание';name=(Norm $a.name)}) } } }
$qp=@{}; for($i=0;$i -lt $courses.Count;$i++){ $qp["courseids[$i]"]=$courses[$i].id }
$qz=Invoke-Moodle 'mod_quiz_get_quizzes_by_courses' $qp
foreach($q in $qz.quizzes){ if($q.timeclose -and [int64]$q.timeclose -ge $now){
  $items.Add([pscustomobject]@{when=[int64]$q.timeclose;course=(CName $q.course);kind='Квиз/экзамен';name=(Norm $q.name)}) } }
$ev=Invoke-Moodle 'core_calendar_get_action_events_by_timesort' @{ timesortfrom=$now; limitnum=50 }
foreach($e in $ev.events){ $items.Add([pscustomobject]@{when=[int64]$e.timesort;course=$e.course.shortname;kind='Событие';name=(Norm $e.name)}) }
$rank=@{'Задание'=0;'Квиз/экзамен'=0;'Событие'=1}; $best=@{}
foreach($it in $items){ $day=[DateTimeOffset]::FromUnixTimeSeconds($it.when).ToString('yyyyMMdd'); $key="$($it.course)|$($it.name)|$day"
  if(-not $best.ContainsKey($key) -or $rank[$it.kind] -lt $rank[$best[$key].kind]){ $best[$key]=$it } }
$clean=$best.Values | Sort-Object when
$lines=New-Object System.Collections.Generic.List[string]
$lines.Add("ДЕДЛАЙНЫ MURDOCH — обновлено $((Get-Date).ToString('dd.MM.yyyy HH:mm'))"); $lines.Add(('='*64))
$urgent=New-Object System.Collections.Generic.List[string]
foreach($it in $clean){ $dt=[DateTimeOffset]::FromUnixTimeSeconds($it.when).ToLocalTime()
  $days=[math]::Floor((($dt-[DateTimeOffset]::Now).TotalDays))
  $flag= if($days -le 1){'!!! '}elseif($days -le 3){'!!  '}elseif($days -le 7){'!   '}else{'    '}
  $lines.Add(("{0}{1}  ({2,2} дн.)  [{3}]  {4}: {5}" -f $flag,$dt.ToString('dd.MM HH:mm'),$days,$it.course,$it.kind,$it.name))
  if($days -le 3){ $urgent.Add(("• {0} ({1} дн.) [{2}] {3}" -f $dt.ToString('dd.MM HH:mm'),$days,$it.course,$it.name)) } }
$report=($lines -join "`r`n")
$desktop=[Environment]::GetFolderPath('Desktop')
Set-Content -Path (Join-Path $desktop 'Дедлайны Murdoch.txt') -Value $report -Encoding utf8
$report | Write-Output
if($urgent.Count -gt 0){ ""; "<<URGENT>>"; $urgent | ForEach-Object { $_ } }
```

### Файл `notify.ps1` (утренний попап при близком дедлайне)
```powershell
$ErrorActionPreference='Stop'; $root=$PSScriptRoot
$out=& powershell -ExecutionPolicy Bypass -File (Join-Path $root 'briefing.ps1')
$text=($out -join "`n"); $urgent=@()
if($text -match '<<URGENT>>'){ $after=($text -split '<<URGENT>>',2)[1]
  $urgent=($after -split "`n") | Where-Object { $_.Trim().StartsWith('•') } }
if($urgent.Count -gt 0){
  $msg="Скоро дедлайны в Murdoch:`n`n"+($urgent -join "`n")+"`n`nПолный список — на рабочем столе: «Дедлайны Murdoch.txt»"
  try{ $sh=New-Object -ComObject WScript.Shell; [void]$sh.Popup($msg,60,'Напоминание Murdoch',0x40) }
  catch{ Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.MessageBox]::Show($msg,'Напоминание Murdoch') | Out-Null } }
```
(Сохрани `briefing.ps1` и `notify.ps1` в UTF-8 **с BOM** — см. выше.)

---

## 4. Проверка API (сквозной тест — обязательно · Windows; macOS-тест — в разделе 5м)
```powershell
. C:\Projects\murdoch-moodle\moodle.ps1
(Invoke-Moodle 'core_webservice_get_site_info') | Select-Object sitename,fullname,userid,release,downloadfiles,@{n='funcs';e={$_.functions.Count}}
Invoke-Moodle 'core_enrol_get_users_courses' @{ userid=$script:MoodleUserId } | Select-Object id,shortname,fullname
```
Ожидаемо: имя пользователя, `downloadfiles=1`, ~450 функций и список его курсов. Затем прогони
`briefing.ps1` — на рабочем столе появится «Дедлайны Murdoch.txt». Скачай один любой файл материалов
(`core_course_get_contents` → возьми `fileurl` → `Get-MoodleFile`), чтобы подтвердить доступ к материалам.

## 5. Напоминания (Планировщик Windows)
```powershell
$action=New-ScheduledTaskAction -Execute 'powershell.exe' -Argument '-NoProfile -WindowStyle Hidden -ExecutionPolicy Bypass -File "C:\Projects\murdoch-moodle\notify.ps1"'
$trigger=New-ScheduledTaskTrigger -Daily -At 8:00am
$settings=New-ScheduledTaskSettingsSet -StartWhenAvailable -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries
$principal=New-ScheduledTaskPrincipal -UserId $env:USERNAME -LogonType Interactive -RunLevel Limited
Register-ScheduledTask -TaskName 'MurdochDeadlineReminder' -Action $action -Trigger $trigger -Settings $settings -Principal $principal -Force
```
Проверь: `Get-ScheduledTaskInfo -TaskName 'MurdochDeadlineReminder'` (должно быть NextRunTime на завтра 08:00).
Для проверки попапа запусти `notify.ps1` в фоне (`Start-Process`), окно само закроется через 60 сек.

## 5м. macOS-ветка (полная реализация — Python + launchd)

> Делай ЭТО вместо разделов 3–5, если ОС = macOS (для Linux — то же, только напоминание через
> `notify-send`/cron вместо osascript/launchd). Python3 на macOS уже есть (`/usr/bin/python3`).

### Грабли macOS (учти СРАЗУ)
- **Папка проекта — `~/murdoch-moodle` (корень home), НЕ в `~/Documents` и НЕ на `~/Desktop`.** Причины:
  (1) `~/Desktop` и `~/Documents` часто синкаются в **iCloud** → токен утёк бы в облако; (2) launchd-агент
  под TCC может не получить доступ к `~/Documents` без Full Disk Access.
- Файл дедлайнов на `~/Desktop` — можно (это не секрет). Токен — только в `~/murdoch-moodle`, права `600`.
- Первый показ уведомления/диалога из launchd может попросить разрешение (Automation) — это норм, разреши.

### Шаг 1 — декод токена (из файла, без base64 в команде)
Сначала положи base64 из сетевой записи в `~/murdoch-moodle/.b64.tmp` **файл-инструментом (Write)**, потом:
```bash
DIR="$HOME/murdoch-moodle"; mkdir -p "$DIR"; chmod 700 "$DIR"
openssl base64 -d -A -in "$DIR/.b64.tmp" | awk -F':::' '{printf "%s",$2}' > "$DIR/.moodle_token"
chmod 600 "$DIR/.moodle_token"; rm -f "$DIR/.b64.tmp"
printf 'token stored, length=%s\n' "$(wc -c < "$DIR/.moodle_token" | tr -d ' ')"   # должно быть 32
```

### Файл `~/murdoch-moodle/moodle.py` (обёртка API + скачивание; userid сам)
```python
#!/usr/bin/env python3
import json, os, urllib.parse, urllib.request
BASE = "https://moodleprod.murdoch.edu.au"
_DIR = os.path.dirname(os.path.abspath(__file__))
TOKEN = open(os.path.join(_DIR, ".moodle_token")).read().strip()

def call(fn, params=None, **kw):
    data = {"wstoken": TOKEN, "wsfunction": fn, "moodlewsrestformat": "json"}
    data.update({k: str(v) for k, v in {**(params or {}), **kw}.items()})   # params — для ключей вида courseids[0]
    body = urllib.parse.urlencode(data).encode()
    with urllib.request.urlopen(BASE + "/webservice/rest/server.php", body, timeout=30) as r:
        out = json.loads(r.read().decode())
    if isinstance(out, dict) and "exception" in out:
        raise RuntimeError(f"Moodle API [{out.get('errorcode')}]: {out.get('message')}")
    return out

def get_file(fileurl, outpath):                       # скачать материал (fileurl из core_course_get_contents)
    sep = "&" if "?" in fileurl else "?"
    urllib.request.urlretrieve(f"{fileurl}{sep}token={TOKEN}", outpath)   # токен как query-параметр

USERID = call("core_webservice_get_site_info")["userid"]   # свой userid, без хардкода
```

### Файл `~/murdoch-moodle/briefing.py` (все дедлайны → отчёт на Рабочий стол)
```python
#!/usr/bin/env python3
import os, sys, time, datetime, html, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import moodle

def norm(s):
    if not s: return ""
    x = html.unescape(s).strip()
    x = re.sub(r'\s*\(Due[^)]*\)', '', x); x = re.sub(r'\s+is due\s*$', '', x)
    return re.sub(r'\s+', ' ', x).strip()

def safe(fn, *a, **k):                                 # один неактивный web-service не должен ронять весь отчёт
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

lines = [f"ДЕДЛАЙНЫ MURDOCH — обновлено {datetime.datetime.now():%d.%m.%Y %H:%M}", "=" * 64]
urgent = []
for when, course, kind, name in sorted(best.values()):
    dt = datetime.datetime.fromtimestamp(when); days = (dt - datetime.datetime.now()).days
    flag = "!!! " if days <= 1 else "!!  " if days <= 3 else "!   " if days <= 7 else "    "
    lines.append(f"{flag}{dt:%d.%m %H:%M}  ({days:2} дн.)  [{course}]  {kind}: {name}")
    if days <= 3: urgent.append(f"• {dt:%d.%m %H:%M} ({days} дн.) [{course}] {name}")

report = "\n".join(lines)
open(os.path.join(os.path.expanduser("~"), "Desktop", "Дедлайны Murdoch.txt"), "w").write(report)
print(report)
if urgent: print("\n<<URGENT>>\n" + "\n".join(urgent))
```

### Файл `~/murdoch-moodle/notify.sh` (утренний попап при близком дедлайне)
```bash
#!/usr/bin/env bash
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OUT="$(/usr/bin/python3 "$DIR/briefing.py" 2>>"$DIR/launchd.err")"
URGENT="$(printf '%s\n' "$OUT" | awk '/<<URGENT>>/{f=1;next} f&&/^•/{print}')"
[ -z "$URGENT" ] && exit 0
export MURDOCH_MSG="Скоро дедлайны в Murdoch:
$URGENT

Полный список — на Рабочем столе: «Дедлайны Murdoch.txt»"
export MURDOCH_SHORT="$(printf '%s' "$URGENT" | tr '\n' ' ' | cut -c1-180)"
# передаём текст через env (system attribute) — надёжнее, чем экранировать кавычки/переносы в -e
/usr/bin/osascript <<'OSA' 2>/dev/null || true
display notification (system attribute "MURDOCH_SHORT") with title "Напоминание Murdoch"
OSA
/usr/bin/osascript <<'OSA' 2>/dev/null || true
display dialog (system attribute "MURDOCH_MSG") with title "Напоминание Murdoch" buttons {"OK"} default button 1 giving up after 60
OSA
```
`chmod +x ~/murdoch-moodle/notify.sh`. (Кириллица в `.py/.sh` на Маке — просто UTF-8, BOM НЕ нужен; BOM только для Windows PowerShell 5.1.)

### Сквозной тест (macOS)
```bash
cd ~/murdoch-moodle
/usr/bin/python3 -c "import moodle,json; s=moodle.call('core_webservice_get_site_info'); \
print(s['fullname'], '| userid', s['userid'], '| downloadfiles', s.get('downloadfiles'), '| funcs', len(s['functions']))"
/usr/bin/python3 briefing.py    # на Рабочем столе появится «Дедлайны Murdoch.txt»
```
Ожидаемо: имя пользователя, `downloadfiles=1`, ~450 функций, список дедлайнов. Проверь материалы: возьми
`fileurl` из `core_course_get_contents` и скачай `moodle.get_file(url, "/tmp/test.pdf")`.

### Напоминание — launchd (LaunchAgent, 08:00 ежедневно)
```bash
PL="$HOME/Library/LaunchAgents/com.murdoch.deadline.plist"
cat > "$PL" <<PLIST
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0"><dict>
  <key>Label</key><string>com.murdoch.deadline</string>
  <key>ProgramArguments</key><array><string>/bin/bash</string><string>$HOME/murdoch-moodle/notify.sh</string></array>
  <key>StartCalendarInterval</key><dict><key>Hour</key><integer>8</integer><key>Minute</key><integer>0</integer></dict>
  <key>StandardErrorPath</key><string>$HOME/murdoch-moodle/launchd.err</string>
  <key>StandardOutPath</key><string>$HOME/murdoch-moodle/launchd.out</string>
</dict></plist>
PLIST
launchctl bootout "gui/$(id -u)/com.murdoch.deadline" 2>/dev/null || true   # идемпотентно: снять старую
launchctl bootstrap "gui/$(id -u)" "$PL"                                    # ставим в GUI-домен (иначе диалог не покажется)
launchctl enable   "gui/$(id -u)/com.murdoch.deadline"
launchctl kickstart -k "gui/$(id -u)/com.murdoch.deadline"                  # прогон сейчас для проверки попапа
```
Проверь: `launchctl print "gui/$(id -u)/com.murdoch.deadline" | grep -E 'state|next'`. Если попап не вышел —
Системные настройки → Конфиденциальность → Automation/Уведомления → разреши Терминалу/osascript.

---

## 6. Постоянная память (чтобы новые сессии сразу имели доступ)
Создай в папке проекта короткие файлы:
- `ACCESS.env` — базовый URL, `MOODLE_USERID` (реальный, из site_info), путь к `.moodle_token`, дата
  истечения токена, пометка «вход только SSO».
- `CLAUDE.md` — как звать пользователя, как пользоваться `moodle.ps1` (Windows) / `moodle.py` (macOS), состав файлов, **раздел
  «Обновление токена»** (повтори процедуру из раздела 2), раздел «Известные грабли» (раздел 7 ниже),
  и «Текущий статус».
- `README.md` — для пользователя-непрограммиста: что умеет, что работает само (08:00), как просить помощи.
Также, если работаешь в Claude Code с файловой памятью — добавь короткую заметку о проекте в свою память.

## 7. Известные грабли (не наступай повторно)
- **Токен — секрет.** В чат не выводить; в git не коммитить; папку держать **вне облачных синков**
  (Windows: OneDrive; **macOS: `~/Desktop` и `~/Documents` = iCloud** → токен только в `~/murdoch-moodle`).
  Права на файл токена — `600`.
- **base64 токена ≡ сам токен.** НЕ подставляй base64/токен как аргумент команды (осядет в истории оболочки
  и транскрипте tool-call). Всегда: base64 → во временный файл (Write-инструментом) → декод из файла → удалить temp.
- **Токен** живёт ограниченно (у Murdoch по умолчанию ~до конца лета; проверь в Moodle → Preferences →
  Security keys, строка «Moodle mobile web service», колонка Valid until). Истёк/сброшен → повтори раздел 2.
  Полезно: в `briefing` предупреждать за ~14 дней до истечения.
- **Пароль/MFA — вводит пользователь сам**; ты пароли не вводишь ни при каких условиях.
- **Робастность отчёта:** оборачивай КАЖДЫЙ вызов web-service (assign/quiz/calendar) в try/catch — если какая-то
  функция не включена на сайте, отчёт должен продолжить с доступным (в `briefing.py` это `safe()`; в PowerShell
  оберни каждый `Invoke-Moodle` в `try{}catch{}`).
- **Windows:** `.ps1` с кириллицей — только **UTF-8 с BOM**; скачивание файлов — **TLS 1.2** +
  `WebClient.DownloadFile` (имена с пробелами и `[ ]`). **macOS/Linux:** `.py/.sh` — обычный UTF-8 (BOM НЕ нужен).
- **macOS launchd:** ставить в домен `gui/$(id -u)` (иначе диалог/уведомление не покажутся); `bootout` перед
  `bootstrap` (идемпотентность); первый показ попапа может запросить разрешение Automation/Уведомления — норм.
- **Приватность/ToS:** это доступ к **своему** аккаунту своим личным токеном (личное использование). Чужие
  токены/логины в этот файл не попадают.

## 8. Тьютор-режим (как помогать по заданию)
Чтобы помочь с конкретной работой: `core_course_get_contents` нужного курса → найди модули с методичкой/
рубрикой (ищи по названиям: rubric, guidelines, brief, assessment, criteria) → скачай их `Get-MoodleFile` →
прочитай → помогай строго по реальным критериям рубрики, а не «в общем». Дедлайн и описание задания бери
из `mod_assign_get_assignments`.

---
Когда всё проверено — отчитайся пользователю простыми словами: какие курсы видны, ближайшие дедлайны,
что напоминания включены, и предложи помочь с самой срочной работой.
