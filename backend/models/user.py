from dataclasses import dataclass

@dataclass
class User:
    email: str
    password_hash: str
    reset_token: str = None
    reset_token_expiry: str = None
    failed_attempts: int = 0
    account_locked: bool = False