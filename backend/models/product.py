from dataclasses import dataclass, field

@dataclass
class Product:
    name: str
    price: float
    description: str
    categories: list = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "price": self.price,
            "description": self.description,
            "categories": self.categories
        }