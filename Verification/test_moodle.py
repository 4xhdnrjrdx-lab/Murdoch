import importlib.util,unittest,tempfile,urllib.parse
from pathlib import Path
from unittest.mock import patch
p=Path(__file__).resolve().parents[1]/'Access/Moodle/moodle.py'
spec=importlib.util.spec_from_file_location('murdoch_moodle',p);module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
class Response:
 def __init__(self,data):self.data=data;self.offset=0
 def __enter__(self):return self
 def __exit__(self,*a):pass
 def read(self,n=-1):
  if n<0:out=self.data[self.offset:];self.offset=len(self.data);return out
  out=self.data[self.offset:self.offset+n];self.offset+=len(out);return out
class MoodleTests(unittest.TestCase):
 def test_mutations_blocked_before_token_read(self):
  c=module.Client('/nonexistent')
  for operation in ['mod_assign_submit_for_grading','core_group_add_group_members','mod_forum_add_discussion']:
   with self.assertRaises(module.MoodleError) as e:c.call(operation)
   self.assertEqual(e.exception.code,'operation_not_allowed')
 def test_reserved_fields_blocked(self):
  with self.assertRaises(module.MoodleError) as e:module.Client('/missing').call('core_webservice_get_site_info',{'wstoken':'do-not-use'})
  self.assertEqual(e.exception.code,'reserved_parameter')
 def test_error_does_not_echo_sensitive_server_message(self):
  c=module.Client('/missing')
  with patch.object(c,'_token',return_value='synthetic-key'),patch.object(c.opener,'open',return_value=Response(b'{"exception":"moodle_exception","errorcode":"invalidtoken","message":"private-value"}')):
   with self.assertRaises(module.MoodleError) as e:c.call('core_webservice_get_site_info')
   self.assertEqual(e.exception.code,'invalidtoken');self.assertNotIn('private-value',str(e.exception))
 def test_file_host_and_outline_blocked(self):
  c=module.Client('/missing')
  for url,code in [('https://example.com/webservice/pluginfile.php/1/a.mp4','file_url_not_allowed'),('https://moodleprod.murdoch.edu.au/webservice/pluginfile.php/1/Unit%20Outline.pdf','unit_outline_redownload_blocked')]:
   with self.assertRaises(module.MoodleError) as e:c.get_file(url,'unused')
   self.assertEqual(e.exception.code,code)
 def test_redirect_blocked(self):
  with self.assertRaises(module.MoodleError):module.NoRedirect().redirect_request(None,None,None,None,None,None)
 def test_read_request_contains_only_expected_function(self):
  c=module.Client('/missing')
  with patch.object(c,'_token',return_value='synthetic-key'),patch.object(c.opener,'open',return_value=Response(b'{"userid":257560}')) as network:
   self.assertEqual(c.call('core_webservice_get_site_info')['userid'],257560)
   url,body=network.call_args.args;self.assertEqual(url,module.BASE+'/webservice/rest/server.php')
   self.assertEqual(urllib.parse.parse_qs(body.decode())['wsfunction'],['core_webservice_get_site_info'])
if __name__=='__main__':unittest.main()
