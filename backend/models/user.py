from dataclasses import dataclass
from typing import Optional
import datetime

@dataclass
class User:
    email: str
    password: str
    reset_token: Optional[str] = None
    reset_token_expiry: Optional[datetime.datetime] = None