from abc import ABC, abstractmethod
from typing import List, Optional
from src.models.cart_item import CartItem

class CartRepository(ABC):
    
    @abstractmethod
    def get_cart_by_user_id(self, user_id: int) -> List[CartItem]:
        """Get all cart items for a specific user"""
        pass
    
    @abstractmethod
    def add_item(self, cart_item: CartItem) -> CartItem:
        """Add an item to the cart"""
        pass
    
    @abstractmethod
    def update_item_quantity(self, user_id: int, product_id: int, quantity: int) -> bool:
        """Update the quantity of a specific item in the cart"""
        pass
    
    @abstractmethod
    def remove_item(self, user_id: int, product_id: int) -> bool:
        """Remove a specific item from the cart"""
        pass
    
    @abstractmethod
    def clear_cart(self, user_id: int) -> bool:
        """Remove all items from the cart for a specific user"""
        pass
    
    @abstractmethod
    def get_item(self, user_id: int, product_id: int) -> Optional[CartItem]:
        """Get a specific item from the cart"""
        pass