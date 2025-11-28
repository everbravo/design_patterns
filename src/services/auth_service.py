from typing import Optional
from src.strategies.auth_strategy import AuthStrategy

class AuthService:
    
    def __init__(self, auth_strategy: AuthStrategy):
        self.auth_strategy = auth_strategy
    
    def login(self, username: str, password: str) -> Optional[str]:
        return self.auth_strategy.authenticate(username, password)
    
    def validate_token(self, token: str) -> bool:
        return self.auth_strategy.validate_token(token)