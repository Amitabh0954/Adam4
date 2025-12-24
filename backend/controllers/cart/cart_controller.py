```python  
"""
Cart Controller
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.services.cart.cart_service import CartService
from backend.repositories.cart.cart_repository import CartRepository
from backend.config.database import get_db

router = APIRouter()

@router.post("/cart/add", response_model=dict)
def add_product_to_cart(product_id: int, user_id: int, quantity: int = 1, db: Session = Depends(get_db)):
    cart_repository = CartRepository(db)
    cart_service = CartService(cart_repository)
    
    try:
        cart_item = cart_service.add_product_to_cart(user_id, product_id, quantity)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    return {"message": "Product added to cart", "cart_item": {"product_id": cart_item.product_id, "quantity": cart_item.quantity, "cart_id": cart_item.cart_id}}

@router.post("/cart/remove", response_model=dict)
def remove_product_from_cart(product_id: int, user_id: int, db: Session = Depends(get_db)):
    cart_repository = CartRepository(db)
    cart_service = CartService(cart_repository)
    
    try:
        cart_service.remove_product_from_cart(user_id, product_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    return {"message": "Product removed from cart"}

@router.post("/cart/modify_quantity", response_model=dict)
def modify_product_quantity(product_id: int, user_id: int, quantity: int, db: Session = Depends(get_db)):
    cart_repository = CartRepository(db)
    cart_service = CartService(cart_repository)

    try:
        cart_service.modify_product_quantity(user_id, product_id, quantity)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    return {"message": "Product quantity updated", "product_id": product_id, "quantity": quantity}

@router.get("/cart", response_model=dict)
def get_cart(user_id: int, db: Session = Depends(get_db)):
    cart_repository = CartRepository(db)
    cart_service = CartService(cart_repository)

    try:
        cart = cart_service.get_cart(user_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    return {"cart": {"cart_id": cart.id, "items": [{"product_id": item.product_id, "quantity": item.quantity} for item in cart.items]}}
```