#!/usr/bin/env python3
"""Exercise real publisher against disposable Git remote and two independent clones."""
import json,subprocess,sys,tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
TEMP=Path(tempfile.mkdtemp(prefix='murdoch-concurrent-'))
PYTHON=sys.executable

def run(cwd,*args,ok=True):
 r=subprocess.run(args,cwd=cwd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
 if ok and r.returncode:raise RuntimeError('Command failed: '+repr(args)+'\n'+r.stdout[-3000:])
 return r
origin=TEMP/'origin.git';a=TEMP/'chat-a';b=TEMP/'chat-b';final=TEMP/'final'
run(TEMP,'git','clone','--bare',str(ROOT),str(origin))
for clone in [a,b]:
 run(TEMP,'git','clone',str(origin),str(clone));run(clone,PYTHON,'scripts/sync.py','configure')
 run(clone,'git','config','user.name','Study verification');run(clone,'git','config','user.email','verification@example.invalid')
pa='BUS219/2026-TSD/HISTORY.md';pb='BUS230/2026-TSD/HISTORY.md'
old_a=(a/pa).read_text();old_b=(b/pb).read_text()
(a/pa).write_text(old_a+'\nVerification: independent BUS219 change A.\n')
(b/pb).write_text(old_b+'\nVerification: independent BUS230 change B.\n')
# In a shared tree, unrelated dirty work must block publication and remain untouched.
foreign=a/'BUS225/2026-TSD/HISTORY.md';foreign_original=foreign.read_text();foreign.write_text(foreign_original+'\nVerification foreign work.\n')
r=run(a,PYTHON,'scripts/sync.py','publish','--message','test A','--paths','BUS219/2026-TSD',ok=False)
assert r.returncode and 'outside your paths' in r.stdout
assert 'Verification foreign work.' in foreign.read_text()
foreign.write_text(foreign_original)
run(a,PYTHON,'scripts/sync.py','publish','--message','test A','--paths','BUS219/2026-TSD')
# B started from the same remote head. Its uncommitted work is preserved on stale-main refusal.
r=run(b,PYTHON,'scripts/sync.py','publish','--message','test B','--paths','BUS230/2026-TSD',ok=False)
assert r.returncode and 'Remote main advanced' in r.stdout
assert 'independent BUS230 change B.' in (b/pb).read_text()
# Commit only the course on its own branch, integrate main first, then refresh derived files.
run(b,'git','switch','-c','verification-bus230');run(b,'git','add','--',pb);run(b,'git','commit','-m','test B course edit')
branch_b=run(b,'git','rev-parse','HEAD').stdout.strip()
run(b,'git','fetch','origin');run(b,'git','switch','main');run(b,'git','pull','--ff-only');run(b,'git','merge','--no-edit','verification-bus230')
run(b,PYTHON,'scripts/sync.py','publish','--message','test B integrated','--paths','BUS230/2026-TSD')
run(TEMP,'git','clone',str(origin),str(final));verify=run(final,PYTHON,'scripts/verify.py')
assert (final/pa).read_text()==old_a+'\nVerification: independent BUS219 change A.\n'
assert (final/pb).read_text()==old_b+'\nVerification: independent BUS230 change B.\n'
run(final,'git','merge-base','--is-ancestor',branch_b,'HEAD')
report={'checked_at':'2026-10-07 Asia/Dubai','result':'PASS','remote':'disposable local bare remote, not production main','clones':2,'cases':['foreign shared-tree edits block publisher without overwrite','stale remote blocks uncommitted publication without overwrite','course branch merges with updated main, keeps both courses','regenerated manifest and fresh final clone pass verify'],'test_directory':str(TEMP),'verification':verify.stdout.strip()}
(ROOT/'Verification/CONCURRENT_REPORT.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(report,ensure_ascii=False,indent=2))
