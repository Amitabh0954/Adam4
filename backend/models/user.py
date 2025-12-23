from dataclasses import dataclass

@dataclass
class User:
    email: str
    password_hash: str
    failed_attempts: int = 0
    account_locked: bool = False