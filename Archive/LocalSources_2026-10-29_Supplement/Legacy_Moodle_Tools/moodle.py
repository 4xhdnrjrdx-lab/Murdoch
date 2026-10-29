#!/usr/bin/env python3
"""Обёртка Moodle Web Services (Murdoch). userid определяется сам, без хардкода."""
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

def get_file(fileurl, outpath):                       # скачать материал курса
    sep = "&" if "?" in fileurl else "?"
    urllib.request.urlretrieve(f"{fileurl}{sep}token={TOKEN}", outpath)

USERID = call("core_webservice_get_site_info")["userid"]   # свой userid
