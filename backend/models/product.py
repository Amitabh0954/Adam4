from dataclasses import dataclass

@dataclass
class Product:
    name: str
    price: float
    description: str

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "price": self.price,
            "description": self.description
        }