#!/usr/bin/env python3
"""Murdoch Moodle: explicit read operations, external secrets, no network on import."""
import argparse,base64,getpass,json,os,re,sys,urllib.parse,urllib.request,urllib.error
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
BASE='https://moodleprod.murdoch.edu.au'
ALLOWED=frozenset({'core_webservice_get_site_info','core_enrol_get_users_courses','core_course_get_contents','mod_assign_get_assignments','mod_assign_get_submission_status','core_group_get_course_user_groups','mod_forum_get_forums_by_courses','mod_forum_get_forum_discussions','core_calendar_get_calendar_events','gradereport_user_get_grade_items','mod_quiz_get_quizzes_by_courses','mod_quiz_get_user_attempts'})
class MoodleError(RuntimeError):
 def __init__(self,code):self.code=code;super().__init__('Moodle read failed: '+code)
class NoRedirect(urllib.request.HTTPRedirectHandler):
 def redirect_request(self,*args,**kw):raise MoodleError('redirect_blocked')
class Client:
 def __init__(self,token_file=None):
  config_path=ROOT/'Access/Moodle/config.json'
  try: config=json.loads(config_path.read_text()) if config_path.exists() else {}
  except (OSError,ValueError):raise MoodleError('invalid_local_config') from None
  value=token_file or os.environ.get('MOODLE_TOKEN_FILE') or config.get('token_file') or ROOT/'.secrets/moodle.token'
  self.token_file=Path(value).expanduser()
  if not self.token_file.is_absolute():self.token_file=ROOT/self.token_file
  self.opener=urllib.request.build_opener(NoRedirect())
 def _token(self):
  try:t=self.token_file.read_text().strip()
  except OSError:raise MoodleError('token_file_unavailable') from None
  if not re.fullmatch(r'[A-Za-z0-9_-]{20,256}',t):raise MoodleError('invalid_local_token_format')
  return t
 def call(self,fn,params=None):
  if fn not in ALLOWED:raise MoodleError('operation_not_allowed')
  params=params or {}
  if {'wstoken','wsfunction','moodlewsrestformat'} & params.keys():raise MoodleError('reserved_parameter')
  body=urllib.parse.urlencode({'wstoken':self._token(),'wsfunction':fn,'moodlewsrestformat':'json',**params}).encode()
  try:
   with self.opener.open(BASE+'/webservice/rest/server.php',body,timeout=30) as r:out=json.load(r)
  except MoodleError:raise
  except (urllib.error.URLError,OSError,ValueError):raise MoodleError('network_or_response_error') from None
  if isinstance(out,dict) and 'exception' in out:
   code=out.get('errorcode','api_error');raise MoodleError(code if re.fullmatch(r'[a-zA-Z0-9_]{1,60}',code) else 'api_error')
  return out
 def get_file(self,url,destination):
  u=urllib.parse.urlsplit(url)
  if u.scheme!='https' or u.netloc!='moodleprod.murdoch.edu.au' or not u.path.startswith('/webservice/pluginfile.php/'):
   raise MoodleError('file_url_not_allowed')
  if re.search(r'unit[\s_\-]*outline',urllib.parse.unquote(u.path),re.I):raise MoodleError('unit_outline_redownload_blocked')
  q=urllib.parse.parse_qsl(u.query,keep_blank_values=True)
  if any(k.lower() in {'token','wstoken'} for k,v in q):raise MoodleError('url_already_contains_secret')
  q.append(('token',self._token()));address=urllib.parse.urlunsplit(u._replace(query=urllib.parse.urlencode(q)))
  p=Path(destination);p.parent.mkdir(parents=True,exist_ok=True);tmp=p.with_suffix(p.suffix+'.partial')
  try:
   with self.opener.open(address,timeout=60) as r,tmp.open('wb') as out:
    while b:=r.read(1024*1024):out.write(b)
   tmp.replace(p)
  except MoodleError:tmp.unlink(missing_ok=True);raise
  except (urllib.error.URLError,OSError):tmp.unlink(missing_ok=True);raise MoodleError('file_download_error') from None

def decode_mobile_location(value):
 u=urllib.parse.urlsplit(value.strip())
 if u.scheme!='moodlemobile':raise MoodleError('invalid_mobile_callback')
 encoded=urllib.parse.parse_qs(u.query).get('token',[None])[0]
 if not encoded and u.netloc.startswith('token='):encoded=urllib.parse.unquote(u.netloc[6:]+u.path)
 if not encoded:raise MoodleError('invalid_mobile_callback')
 try:
  fields=base64.b64decode(encoded+'='*(-len(encoded)%4),validate=True).decode().split(':::')
 except (ValueError,UnicodeError):raise MoodleError('invalid_mobile_callback') from None
 if len(fields)<2 or not re.fullmatch(r'[A-Za-z0-9_-]{20,256}',fields[1]):raise MoodleError('invalid_mobile_callback')
 return fields[1]

def configure(path,mobile=False):
 if not sys.stdin.isatty():raise MoodleError('interactive_terminal_required')
 p=Path(path).expanduser();p.parent.mkdir(parents=True,exist_ok=True,mode=0o700)
 value=getpass.getpass('Mobile Location callback (hidden): ' if mobile else 'Moodle token (hidden; retrieve from Apple Passwords): ').strip()
 t=decode_mobile_location(value) if mobile else value
 if not re.fullmatch(r'[A-Za-z0-9_-]{20,256}',t):raise MoodleError('invalid_local_token_format')
 # Check it before replacing any working key. Temporary key remains outside tracked files.
 tmp=p.with_name(p.name+'.new');fd=os.open(tmp,os.O_WRONLY|os.O_CREAT|os.O_TRUNC,0o600)
 try:
  with os.fdopen(fd,'w') as f:f.write(t+'\n')
  os.chmod(tmp,0o600);info=Client(tmp).call('core_webservice_get_site_info')
  os.replace(tmp,p);os.chmod(p,0o600)
  print('Access verified; token stored locally outside Git. userid:',info.get('userid'))
 finally:tmp.unlink(missing_ok=True)

def main():
 ap=argparse.ArgumentParser();ap.add_argument('command',choices=['check','configure','configure-mobile','download-bus230-videos']);ap.add_argument('--token-file');args=ap.parse_args()
 client=Client(args.token_file)
 try:
  if args.command in {'configure','configure-mobile'}:configure(client.token_file,mobile=args.command=='configure-mobile')
  elif args.command=='check':print(json.dumps({'access':'ok','userid':client.call('core_webservice_get_site_info').get('userid')},ensure_ascii=False))
  else:
   client.call('core_webservice_get_site_info')
   for section in client.call('core_course_get_contents',{'courseid':31305}):
    for mod in section.get('modules',[]):
     for f in mod.get('contents',[]):
      if f.get('mimetype','').startswith('video/'):
       name=f['filename'];path=ROOT/'BUS230/2026-TSD/Materials/Videos'/name
       if path.exists() and path.stat().st_size==f['filesize']:print('Already local:',name);continue
       client.get_file(f['fileurl'],path)
       if path.stat().st_size!=f['filesize']:raise MoodleError('file_size_mismatch')
       print('Saved:',name,path.stat().st_size)
   print('Next: update gap records, render manifest, verify and publish.')
 except MoodleError as e:print(str(e),file=sys.stderr);return 1
 return 0
if __name__=='__main__':sys.exit(main())
