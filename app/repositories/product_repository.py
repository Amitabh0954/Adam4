from app.models.product import Product
from app.repositories.database import db

class ProductRepository:
    def search_query(self, query: str, page: int, per_page: int) -> list[Product]:
        return Product.query.filter(
            (Product.name.ilike(f'%{query}%')) |
            (Product.description.ilike(f'%{query}%')) |
            (Product.category.ilike(f'%{query}%')) |
            (Product.attributes['attributes'].astext.ilike(f'%{query}%'))
        ).paginate(page, per_page, error_out=False).items

    def count_query_results(self, query: str) -> int:
        return Product.query.filter(
            (Product.name.ilike(f'%{query}%')) |
            (Product.description.ilike(f'%{query}%')) |
            (Product.category.ilike(f'%{query}%')) |
            (Product.attributes['attributes'].astext.ilike(f'%{query}%'))
        ).count()
