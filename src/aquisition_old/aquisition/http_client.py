from requests import Session
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

class HttpClient:
    def __init__(self):
        self.session=Session()
        retry=Retry(total=5,status_forcelist=[429,500,502,503,504])
        adapter=HTTPAdapter(max_retries=retry)
        self.session.mount('http://',adapter)
        self.session.mount('https://',adapter)

    def get(self,url,**kwargs):
        return self.session.get(url,allow_redirects=True,**kwargs)
