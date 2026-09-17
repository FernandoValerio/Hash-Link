from abc import ABC, abstractmethod
from requests import Session
from requests.auth import HTTPBasicAuth

class AuthenticationProvider(ABC):
    @abstractmethod
    def apply(self, session: Session) -> Session:
        pass

class BasicAuthProvider(AuthenticationProvider):
    def __init__(self, username:str,password:str):
        self.username=username
        self.password=password

    def apply(self, session: Session) -> Session:
        session.auth = HTTPBasicAuth(self.username,self.password)
        return session

class BearerTokenProvider(AuthenticationProvider):
    def __init__(self, token:str):
        self.token=token

    def apply(self, session: Session) -> Session:
        session.headers['Authorization']=f'Bearer {self.token}'
        return session
