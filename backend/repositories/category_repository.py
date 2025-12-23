from typing import Optional, List
from backend.models.category import Category

class CategoryRepository:
    def __init__(self):
        self.categories = []

    def get_category_by_name(self, name: str) -> Optional[Category]:
        for category in self.categories:
            if category.name == name:
                return category
        return None

    def add_category(self, category: Category) -> None:
        self.categories.append(category)

    def get_all_categories(self) -> List[Category]:
        return self.categories