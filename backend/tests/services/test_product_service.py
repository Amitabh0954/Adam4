```python
import pytest
from backend.services.products.product_service import ProductService
from backend.services.products.category_service import CategoryService

@pytest.fixture
def product_service() -> ProductService:
    return ProductService()

@pytest.fixture
def category_service() -> CategoryService:
    return CategoryService()

def test_add_product(product_service, category_service):
    category_service.add_category("Electronics", None)
    product = product_service.add_product("Test Product", 10.99, "A test product", ["Electronics"])
    assert product.name == "Test Product"
    assert product.price == 10.99
    assert product.description == "A test product"
    assert "Electronics" in product.categories

def test_add_product_with_nonexistent_category(product_service):
    with pytest.raises(ValueError, match="Category Nonexistent does not exist"):
        product_service.add_product("Test Product", 10.99, "A test product", ["Nonexistent"])

def test_is_product_name_taken(product_service, category_service):
    category_service.add_category("Electronics", None)
    product_service.add_product("Test Product", 10.99, "A test product", ["Electronics"])
    assert product_service.is_product_name_taken("Test Product") is True
    assert product_service.is_product_name_taken("Another Product") is False

def test_get_all_products(product_service, category_service):
    category_service.add_category("Electronics", None)
    product_service.add_product("Test Product 1", 10.99, "First test product", ["Electronics"])
    product_service.add_product("Test Product 2", 15.99, "Second test product", ["Electronics"])

    products = product_service.get_all_products()
    assert len(products) == 2
    assert products[0].name == "Test Product 1"
    assert products[0].price == 10.99
    assert products[0].description == "First test product"
    assert "Electronics" in products[0].categories
    assert products[1].name == "Test Product 2"
    assert products[1].price == 15.99
    assert products[1].description == "Second test product"
    assert "Electronics" in products[1].categories

def test_update_product(product_service, category_service):
    category_service.add_category("Electronics", None