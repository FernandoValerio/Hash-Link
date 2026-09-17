from abc import ABC,abstractmethod
class AuthenticationProvider(ABC):
 @abstractmethod
 def apply(self,session): pass
