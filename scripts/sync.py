#!/usr/bin/env python3
"""Conservative sequential publication. Normal push preserves remote concurrent commits."""
import argparse,fcntl,os,subprocess,sys
from pathlib import Path
from base import ROOT,COURSES
ap=argparse.ArgumentParser();ap.add_argument('command',choices=['status','configure','publish']);ap.add_argument('--message');ap.add_argument('--paths',nargs='+',default=[]);a=ap.parse_args()
def run(*args,check=True):return subprocess.run(args,cwd=ROOT,check=check,text=True)
def out(*args):return subprocess.check_output(args,cwd=ROOT,text=True).strip()
def dirty():
 lines=subprocess.check_output(['git','status','--porcelain','-z'],cwd=ROOT).decode().split('\0');res=[]
 for s in lines:
  if s:
   if s[:2].strip() in {'R','C'}:raise RuntimeError('Resolve/stage renames manually first')
   res.append(s[3:])
 return res
def allowed(path,roots):return any(path==x or path.startswith(x.rstrip('/')+'/') for x in roots)
def config():
 for key,val in [('pull.ff','only'),('push.default','simple'),('core.autocrlf','false'),('core.hooksPath','.githooks'),('core.quotepath','false'),('fetch.fsckObjects','true'),('transfer.fsckObjects','true'),('receive.fsckObjects','true')]:run('git','config','--local',key,val)
if a.command=='configure':config();print('Local Git safeguards configured');sys.exit(0)
run('git','fetch','origin')
if a.command=='status':
 head=out('git','rev-parse','HEAD');remote=out('git','rev-parse','origin/main');print('local HEAD:',head,'\norigin/main:',remote,'\nmatch:',head==remote,'\nworking changes:',len(dirty()));sys.exit(0)
if not a.message or not a.paths:ap.error('publish requires --message and explicit --paths')
for p in a.paths:
 if p.startswith('/') or '..' in Path(p).parts:ap.error('paths must be repository-relative')
if out('git','branch','--show-current')!='main':raise SystemExit('Publish only from integration main; merge your course branch explicitly first')
lock=ROOT/out('git','rev-parse','--git-path','murdoch-publish.lock')
with lock.open('w') as f:
 fcntl.flock(f,fcntl.LOCK_EX)
 # A live shared checkout with other edits cannot be safely summarized or staged.
 derived=['README.md','MANIFEST.json']+[c['path']+'/'+n for c in COURSES['courses'] for n in ['README.md','TASKS.md']]
 foreign=[p for p in dirty() if not allowed(p,a.paths+derived)]
 if foreign:raise SystemExit('Uncommitted changes outside your paths; preserved: '+', '.join(foreign))
 run('git','fetch','origin')
 ahead=int(out('git','rev-list','--count','HEAD..origin/main'))
 if ahead and dirty():raise SystemExit('Remote main advanced; commit course edits on a branch and merge latest main before publishing. Nothing overwritten.')
 if ahead:run('git','merge','--no-edit','origin/main')
 run(sys.executable,'scripts/render.py');run(sys.executable,'scripts/verify.py')
 run('git','add','--',*a.paths,*derived)
 run(sys.executable,'scripts/verify.py','--staged')
 if subprocess.run(['git','diff','--cached','--quiet'],cwd=ROOT).returncode:run('git','commit','-m',a.message)
 # Fetch again. Integrate remote commits if it changed; merge conflicts stop without choosing a side.
 for attempt in range(3):
  run('git','fetch','origin')
  if int(out('git','rev-list','--count','HEAD..origin/main')):
   run('git','merge','--no-edit','origin/main')
   run(sys.executable,'scripts/render.py');run(sys.executable,'scripts/verify.py')
   run('git','add','--',*derived)
   if subprocess.run(['git','diff','--cached','--quiet'],cwd=ROOT).returncode:run('git','commit','-m','Refresh derived study overview after concurrent changes')
  pushed=run('git','push','origin','main',check=False)
  if pushed.returncode==0:break
 else:raise SystemExit('Main kept changing or push failed; commits preserved locally. Retry after inspecting origin.')
 remote=out('git','ls-remote','origin','refs/heads/main').split()[0];local=out('git','rev-parse','HEAD')
 if remote!=local:raise SystemExit('Remote advanced after push; your commit is saved, fetch current main before continuation')
 print('VERIFIED main:',remote)
