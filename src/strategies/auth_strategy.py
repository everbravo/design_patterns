from abc import ABC, abstractmethod
from typing import Optional

class AuthStrategy(ABC):
    
    @abstractmethod
    def authenticate(self, username: str, password: str) -> Optional[str]:
        """Authenticate user and return token if successful"""
        pass
    
    @abstractmethod
    def validate_token(self, token: str) -> bool:
        """Validate if token is valid"""
        pass

class SimpleAuthStrategy(AuthStrategy):
    
    def __init__(self):
        self.valid_credentials = {'student': 'desingp'}
        self.valid_token = 'abcd12345'
    
    def authenticate(self, username: str, password: str) -> Optional[str]:
        if username in self.valid_credentials and self.valid_credentials[username] == password:
            return self.valid_token
        return None
    
    def validate_token(self, token: str) -> bool:
        return token == self.valid_token