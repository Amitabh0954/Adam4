from backend.models.category import Category
from backend.repositories.category_repository import CategoryRepository

class CategoryService:
    def __init__(self):
        self.category_repository = CategoryRepository()

    def is_category_exist(self, name: str) -> bool:
        return self.category_repository.get_category_by_name(name) is not None

    def add_category(self, name: str, parent_name: str) -> None:
        parent_category = None
        if parent_name:
            parent_category = self.category_repository.get_category_by_name(parent_name)
            if not parent_category:
                raise ValueError(f"Parent category {parent_name} does not exist")
        category = Category(name=name, parent=parent_category)
        self.category_repository.add_category(category)

    def get_all_categories(self) -> list:
        return self.category_repository.get_all_categories()