#!/usr/bin/env python3
"""Read-only verification of the dated Mac-to-GitHub source map."""
import argparse, hashlib, json, subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--sources', action='store_true', help='Also hash original Mac paths; never modify them')
args = parser.parse_args()
audit = json.loads((ROOT/'Migration/LOCAL_AUDIT_2026-10-29.json').read_text())
errors = []
cache = {}
verified = 0
excluded = 0
for row in audit['rows']:
    action = row['action']
    if action.startswith('excluded_'):
        excluded += 1
    else:
        if action == 'existing_history':
            key = ('blob', row['git_blob'])
            if key not in cache:
                data = subprocess.check_output(['git', 'cat-file', 'blob', row['git_blob']], cwd=ROOT)
                cache[key] = (len(data), hashlib.sha256(data).hexdigest())
        else:
            relative = Path(row['destination'])
            if relative.is_absolute() or '..' in relative.parts:
                errors.append('Unsafe destination: '+row['source'])
                continue
            key = ('file', str(relative))
            if key not in cache:
                try:
                    data = (ROOT/relative).read_bytes()
                    cache[key] = (len(data), hashlib.sha256(data).hexdigest())
                except OSError:
                    errors.append('Missing destination: '+str(relative))
                    continue
        expected = ((row['saved_bytes'], row['saved_sha256'])
                    if action == 'archived_redacted_headers'
                    else (row['bytes'], row['sha256']))
        if cache[key] != expected:
            errors.append('Saved bytes mismatch: '+row['source'])
        else:
            verified += 1
    if args.sources:
        try:
            data = Path(row['source']).read_bytes()
            if (len(data), hashlib.sha256(data).hexdigest()) != (row['bytes'], row['sha256']):
                errors.append('Original changed since audit: '+row['source'])
        except OSError:
            errors.append('Original unavailable: '+row['source'])
if errors:
    print('\n'.join('FAIL: '+x for x in errors))
    raise SystemExit(1)
print(f'PASS: {verified} source entries resolve to verified Git bytes; {excluded} explicit non-source exclusions; originals checked: {args.sources}')
