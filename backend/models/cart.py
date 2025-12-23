from dataclasses import dataclass, field
from typing import Dict

@dataclass
class Cart:
    items: Dict[str, int] = field(default_factory=dict)

    def add_item(self, product_id: str, quantity: int):
        if product_id in self.items:
            self.items[product_id] += quantity
        else:
            self.items[product_id] = quantity

    def remove_item(self, product_id: str):
        if product_id in self.items:
            del self.items[product_id]

    def to_dict(self) -> dict:
        return {"items": self.items}