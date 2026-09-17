class FormAuthenticationProvider:
 def __init__(self,login_url,username,password):
  self.login_url=login_url; self.username=username; self.password=password
 def apply(self,s):
  s.post(self.login_url,data={"username":self.username,"password":self.password}); return s
