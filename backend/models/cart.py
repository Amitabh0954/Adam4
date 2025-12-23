from dataclasses import dataclass
from typing import Dict

@dataclass
class Cart:
    user_id: str
    items: Dict[str, int]  # key: product_id, value: quantity