from dataclasses import dataclass, field
from typing import Optional

@dataclass
class Category:
    name: str
    parent: Optional['Category'] = None

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "parent": self.parent.name if self.parent else None
        }