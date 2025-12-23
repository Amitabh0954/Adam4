from dataclasses import dataclass
from typing import Dict

@dataclass
class Cart:
    user_id: str
    items: Dict[str, int]  # key: product_id, value: quantity

    def total_price(self, product_prices: Dict[str, float]) -> float:
        return sum(quantity * product_prices[product_id] for product_id, quantity in self.items.items())