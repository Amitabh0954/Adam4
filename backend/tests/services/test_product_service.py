import pytest
from backend.services.products.product_service import ProductService

@pytest.fixture
def product_service() -> ProductService:
    return ProductService()

def test_add_product(product_service):
    product = product_service.add_product("Test Product", 10.99, "A test product")
    assert product.name == "Test Product"
    assert product.price == 10.99
    assert product.description == "A test product"

def test_is_product_name_taken(product_service):
    product_service.add_product("Test Product", 10.99, "A test product")
    assert product_service.is_product_name_taken("Test Product") is True
    assert product_service.is_product_name_taken("Another Product") is False

def test_get_all_products(product_service):
    product_service.add_product("Test Product 1", 10.99, "First test product")
    product_service.add_product("Test Product 2", 15.99, "Second test product")

    products = product_service.get_all_products()
    assert len(products) == 2
    assert products[0].name == "Test Product 1"
    assert products[0].price == 10.99
    assert products[0].description == "First test product"
    assert products[1].name == "Test Product 2"
    assert products[1].price == 15.99
    assert products[1].description == "Second test product"

def test_update_product(product_service):
    product_service.add_product("Test Product", 10.99, "A test product")
    updated_product = product_service.update_product("Test Product", 12.99, "An updated test product")
    assert updated_product is not None
    assert updated_product.price == 12.99
    assert updated_product.description == "An updated test product"

def test_update_non_existent_product(product_service):
    updated_product = product_service.update_product("Non Existent Product", 12.99, "An updated test product")
    assert updated_product is None

def test_delete_product(product_service):
    product_service.add_product("Test Product", 10.99, "A test product")
    assert product_service.delete_product("Test Product") is True
    assert product_service.get_all_products() == []

def test_delete_non_existent_product(product_service):
    assert product_service.delete_product("Non Existent Product") is False