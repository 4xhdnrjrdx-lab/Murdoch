#!/usr/bin/env python3
"""Validate bytes, scope, primary sources, current links and common secret leaks."""
import argparse,hashlib,json,re,subprocess,sys,zipfile,io
from pathlib import Path
from urllib.parse import unquote,urlsplit
from base import ROOT,COURSES,read,retained,digest
ap=argparse.ArgumentParser();ap.add_argument('--staged',action='store_true');a=ap.parse_args();errors=[]
def check(ok,msg):
 if not ok:errors.append(msg)
def payload(path):
 if a.staged:
  r=subprocess.run(['git','show',':'+path],cwd=ROOT,stdout=subprocess.PIPE,stderr=subprocess.DEVNULL)
  if r.returncode:raise FileNotFoundError(path)
  return r.stdout
 return (ROOT/path).read_bytes()
try:manifest=json.loads(payload('MANIFEST.json'))
except Exception:print('FAIL: manifest missing or invalid');sys.exit(1)
paths={x['path'] for x in manifest['files']}
check(len(paths)==manifest['file_count'],'Manifest contains duplicate/missing paths')
check(sum(x['bytes'] for x in manifest['files'])==manifest['total_bytes'],'Manifest byte total')
if a.staged:
 actual=set(subprocess.check_output(['git','ls-files','-z'],cwd=ROOT).decode().split('\0'))-{'' ,'MANIFEST.json'}
else:actual={p.relative_to(ROOT).as_posix() for p in retained()}
check(actual==paths,'Retained file set differs from manifest: '+str(sorted(actual^paths)[:8]))
secret_patterns=[rb'(?:wstoken|token|access_token)=[A-Za-z0-9_-]{20,}',rb'gh[pousr]_[A-Za-z0-9]{30,}',rb'github_pat_[A-Za-z0-9_]{30,}',rb'-----BEGIN (?:RSA |OPENSSH |EC )?PRIVATE KEY-----',rb'(?i)(?:TOKEN|PASSWORD|COOKIE)\s*=\s*[\x22\x27][A-Za-z0-9_-]{20,}']
for entry in manifest['files']:
 p=entry['path']
 check(not p.startswith('/') and '..' not in Path(p).parts,'Unsafe manifest path: '+p)
 try:data=payload(p)
 except Exception:errors.append('Missing file: '+p);continue
 check(len(data)==entry['bytes'] and hashlib.sha256(data).hexdigest()==entry['sha256'],'Hash/size mismatch: '+p)
 check(entry['storage']=='git','Unsupported storage, materialized bytes required: '+p)
 check(len(data)<100*1024*1024,'File needs explicit large storage decision: '+p)
 check(not data.startswith(b'version https://git-lfs.github.com/spec/v1\n'),'LFS pointer instead of materialized file: '+p)
 check(not any(x in Path(p).parts for x in {'.secrets','.git','__pycache__'}) and Path(p).name!='.moodle_token','Secret/cache path: '+p)
 texts=[]
 if Path(p).suffix.lower() in {'.md','.json','.yaml','.tsv','.html','.py','.txt','.sh','.js','.css','.example'}:texts=[data]
 if Path(p).suffix.lower() in {'.docx','.pptx','.xlsx'}:
  try:
   z=zipfile.ZipFile(io.BytesIO(data));texts=[z.read(n) for n in z.namelist() if n.endswith(('.xml','.rels'))]
  except zipfile.BadZipFile:errors.append('Corrupt Office ZIP: '+p)
 if any(re.search(pattern,t) for pattern in secret_patterns for t in texts):errors.append('Possible secret: '+p+' (value withheld)')
for c in COURSES['courses']:
 base=ROOT/c['path'];state=read(c['path']+'/TASKS.json')
 check(c['status'] in COURSES['course_states'],'Invalid course state '+c['code'])
 check(c['status'] not in {'успешно завершён','требуется пересдача'} or bool(c.get('result')),'Official result missing '+c['code'])
 check((ROOT/c['status_source']).is_file(),'Missing course source '+c['code'])
 for t in state['tasks']:
  check(t['status'] in state['allowed_states'],'Invalid task state '+c['code']+t['id'])
  check(bool(t['evidence']),'No evidence '+c['code']+t['id'])
  for e in t['evidence']:
   if e.get('path'):check((base/e['path']).is_file(),'Missing evidence '+c['code']+t['id']+': '+e['path'])
  for d in t['deadlines']:
   check(bool(d.get('checked_at')) and bool(d.get('source_label')),'Deadline provenance '+c['code']+t['id'])
   check((base/d['source_path']).is_file(),'Missing deadline source '+c['code']+t['id'])
 # Only maintained records, generated navigation and access docs promise current working links.
 maintained=[base/n for n in ['README.md','CONTEXT.md','TASKS.md','TEAM.md','HISTORY.md','Materials/README.md','Assignments/README.md','Correspondence/README.md']]
 maintained+=[ROOT/n for n in ['README.md','AGENTS.md','RESTORE.md','Access/Moodle/README.md','Migration/README.md','Migration/GAPS.md','Verification/RESTORE_REPORT.md']]
 for p in maintained:
  if not p.exists():errors.append('Required document missing '+str(p.relative_to(ROOT)));continue
  txt=p.read_text()
  for target in re.findall(r'\[[^\]]*\]\(([^\n)]+)\)',txt):
   target=target.strip('<>');url=urlsplit(target)
   if url.scheme or target.startswith('#'):continue
   dest=(p.parent/unquote(url.path)).resolve()
   check(dest.is_relative_to(ROOT) and dest.exists(),'Broken current link '+str(p.relative_to(ROOT))+': '+target)
# Migration destination equivalence: one retained copy for each nonexcluded source.
for row in read('Migration/INVENTORY.json')['files']:
 if row['action']=='excluded':continue
 try:data=payload(row['new_path'])
 except Exception:errors.append('Missing migration destination '+row['old_path']);continue
 check(hashlib.sha256(data).hexdigest()==row['sha256'],'Migration source mismatch '+row['old_path'])
if errors:
 print('\n'.join('FAIL: '+e for e in sorted(set(errors))));sys.exit(1)
print(f'PASS: {len(paths)} files, {manifest["total_bytes"]} bytes; SHA-256, scope, sources, links, states and secret scan')
