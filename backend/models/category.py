from dataclasses import dataclass
from typing import Optional, List

@dataclass
class Category:
    name: str
    parent: Optional[str] = None
    children: List[str] = None

    def __post_init__(self):
        if self.children is None:
            self.children = []