#!/bin/zsh
cd -- "$(dirname -- "$0")" || exit 1
exec /usr/bin/open -a "Google Chrome" "$PWD/record.html"
