"""Local recording page; the server lives independently of the Codex turn."""
from functools import partial
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from urllib.request import urlopen
from urllib.error import URLError
import shutil
import tempfile
import subprocess
import sys
import time
import webbrowser

folder = Path(__file__).resolve().parent
url = 'http://127.0.0.1:8779/record.html'
label = 'edu.bus225.a1.recorder'
live_folder = Path(tempfile.gettempdir()) / 'bus225-a1-live'
live_folder.mkdir(mode=0o700, exist_ok=True)
shutil.copy2(folder / 'record.html', live_folder / 'record.html')

def available():
    try:
        with urlopen(url, timeout=1) as response:
            return b'<title>BUS225' in response.read(3000)
    except (URLError, TimeoutError, OSError):
        return False

if '--server' in sys.argv:
    handler = partial(SimpleHTTPRequestHandler, directory=str(folder))
    try:
        server = ThreadingHTTPServer(('127.0.0.1', 8779), handler)
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    sys.exit(0)

if not available():
    # A session job, with no login item or automatic launch after reboot.
    subprocess.run(['/bin/launchctl', 'remove', label], capture_output=True)
    result = subprocess.run(['/bin/launchctl', 'submit', '-l', label,
                             '--', sys.executable, '-m', 'http.server', '8779', '--bind', '127.0.0.1', '--directory', str(live_folder)],
                            capture_output=True, text=True)
    for _ in range(80):
        if available():
            break
        time.sleep(.1)
    else:
        print('Не удалось открыть страницу записи. Порт 8779 может быть занят.\n'+result.stderr)
        sys.exit(1)

print('Страница записи: '+url+'\nЗапуск завершён. Это окно можно закрыть: запись продолжит работать.')
if '--no-open' not in sys.argv:
    webbrowser.open(url)
