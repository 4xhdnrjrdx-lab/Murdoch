#!/usr/bin/env bash
# Утренний попап, если есть дедлайн в ближайшие 3 дня. Полный список — файл deadlines.txt.
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OUT="$(/usr/bin/python3 "$DIR/briefing.py" 2>>"$DIR/launchd.err")"
URGENT="$(printf '%s\n' "$OUT" | awk '/<<URGENT>>/{f=1;next} f&&/^•/{print}')"
[ -z "$URGENT" ] && exit 0

# Текст пишем в UTF-8 файлы и читаем в AppleScript как «class utf8» — иначе кириллица бьётся в кракозябры.
MSGFILE="$DIR/.msg.tmp"; SHORTFILE="$DIR/.short.tmp"
{
  printf 'Скоро дедлайны в Murdoch (ваше время, Дубай UTC+4):\n\n'
  printf '%s\n' "$URGENT"
  printf '\nПолный список: ~/murdoch-moodle/deadlines.txt\n'
} > "$MSGFILE"
printf '%s' "$URGENT" | tr '\n' ' ' | cut -c1-170 > "$SHORTFILE"

/usr/bin/osascript <<OSA 2>/dev/null || true
set t to (read POSIX file "$SHORTFILE" as «class utf8»)
display notification t with title "Напоминание Murdoch"
OSA
/usr/bin/osascript <<OSA 2>/dev/null || true
set t to (read POSIX file "$MSGFILE" as «class utf8»)
display dialog t with title "Напоминание Murdoch" buttons {"OK"} default button 1 giving up after 90
OSA
rm -f "$MSGFILE" "$SHORTFILE"
