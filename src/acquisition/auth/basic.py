from requests.auth import HTTPBasicAuth
class BasicAuthProvider:
 def __init__(self,u,p): self.u=u; self.p=p
 def apply(self,s): s.auth=HTTPBasicAuth(self.u,self.p); return s
