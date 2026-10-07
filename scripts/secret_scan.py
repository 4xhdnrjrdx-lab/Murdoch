#!/usr/bin/env python3
"""Scan staged contents on course branches without regenerating shared derived files."""
import io,re,subprocess,sys,zipfile
from pathlib import Path
root=Path(__file__).resolve().parents[1]
paths=subprocess.check_output(['git','diff','--cached','--name-only','--diff-filter=ACMR','-z'],cwd=root).decode().split('\0')
patterns=[rb'(?:wstoken|token|access_token)=[A-Za-z0-9_-]{20,}',rb'gh[pousr]_[A-Za-z0-9]{30,}',rb'github_pat_[A-Za-z0-9_]{30,}',rb'-----BEGIN (?:RSA |OPENSSH |EC )?PRIVATE KEY-----',rb'(?i)(?:TOKEN|PASSWORD|COOKIE)\s*=\s*[\x22\x27][A-Za-z0-9_-]{20,}']
errors=[]
for p in filter(None,paths):
 if any(x in Path(p).parts for x in {'.secrets','__pycache__'}) or Path(p).name=='.moodle_token':errors.append('Prohibited path: '+p);continue
 data=subprocess.check_output(['git','show',':'+p],cwd=root);texts=[data]
 if len(data)>=100*1024*1024:errors.append('Large file requires storage decision: '+p)
 if Path(p).suffix.lower() in {'.docx','.pptx','.xlsx'}:
  try:
   z=zipfile.ZipFile(io.BytesIO(data));texts=[z.read(n) for n in z.namelist() if n.endswith(('.xml','.rels'))]
  except zipfile.BadZipFile:errors.append('Corrupt Office file '+p)
 if any(re.search(s,t) for s in patterns for t in texts):errors.append('Possible secret '+p+' (withheld)')
if errors:print('\n'.join(errors));sys.exit(1)
print('Staged secret/size checks passed')
