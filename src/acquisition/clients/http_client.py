from requests import Session
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
class HttpClient:
 def __init__(self):
  self.session=Session(); r=Retry(total=5,status_forcelist=[429,500,502,503,504]); a=HTTPAdapter(max_retries=r); self.session.mount("http://",a); self.session.mount("https://",a)
 def get(self,*a,**k): return self.session.get(*a,**k)
 def post(self,*a,**k): return self.session.post(*a,**k)
