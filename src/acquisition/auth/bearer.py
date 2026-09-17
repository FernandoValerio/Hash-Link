class BearerTokenProvider:
 def __init__(self,t): self.t=t
 def apply(self,s): s.headers["Authorization"]=f"Bearer {self.t}"; return s
