#!/usr/bin/env python3
"""Standard-library study database helpers. All paths are repository-relative."""
import hashlib,json,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
COURSES=json.loads((ROOT/'COURSES.yaml').read_text(encoding='utf-8'))
def read(path):return json.loads((ROOT/path).read_text(encoding='utf-8'))
def write(path,obj):
 p=ROOT/path;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def digest(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for block in iter(lambda:f.read(1024*1024),b''):h.update(block)
 return h.hexdigest()
def retained():
 paths=[]
 for c in COURSES['courses']:
  paths.extend(p for p in (ROOT/c['path']).rglob('*') if p.is_file())
 for folder in ['Archive','Migration','Access','scripts','Verification','.githooks']:
  paths.extend(p for p in (ROOT/folder).rglob('*') if p.is_file())
 paths.extend(ROOT/p for p in ['README.md','AGENTS.md','COURSES.yaml','RESTORE.md','ACCESS_STATUS.json','.gitignore','.gitattributes'] if (ROOT/p).is_file())
 return sorted(set(p for p in paths if '__pycache__' not in p.parts and p.name!='.DS_Store' and p.suffix!='.pyc' and '.secrets' not in p.parts),key=lambda p:p.relative_to(ROOT).as_posix())
def git(*args):return subprocess.check_output(['git','-C',str(ROOT),*args],text=True).strip()
