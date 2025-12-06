from abc import ABC, abstractmethod
from src.models.cart_item import CartItem

class CartObserver(ABC):
    """Abstract base class for cart observers"""
    
    @abstractmethod
    def on_item_added(self, user_id: int, cart_item: CartItem) -> None:
        """Called when an item is added to the cart"""
        pass
    
    @abstractmethod
    def on_item_removed(self, user_id: int, product_id: int) -> None:
        """Called when an item is removed from the cart"""
        pass
    
    @abstractmethod
    def on_quantity_updated(self, user_id: int, product_id: int, old_quantity: int, new_quantity: int) -> None:
        """Called when item quantity is updated"""
        pass
    
    @abstractmethod
    def on_cart_cleared(self, user_id: int) -> None:
        """Called when the entire cart is cleared"""
        pass

class InventoryObserver(CartObserver):
    """Observer that tracks inventory changes based on cart operations"""
    
    def on_item_added(self, user_id: int, cart_item: CartItem) -> None:
        print(f"[INVENTORY] User {user_id} added {cart_item.quantity}x {cart_item.product_name} to cart")
    
    def on_item_removed(self, user_id: int, product_id: int) -> None:
        print(f"[INVENTORY] User {user_id} removed product {product_id} from cart")
    
    def on_quantity_updated(self, user_id: int, product_id: int, old_quantity: int, new_quantity: int) -> None:
        quantity_diff = new_quantity - old_quantity
        action = "increased" if quantity_diff > 0 else "decreased"
        print(f"[INVENTORY] User {user_id} {action} product {product_id} quantity by {abs(quantity_diff)}")
    
    def on_cart_cleared(self, user_id: int) -> None:
        print(f"[INVENTORY] User {user_id} cleared their entire cart")

class AnalyticsObserver(CartObserver):
    """Observer that tracks analytics events for cart operations"""
    
    def on_item_added(self, user_id: int, cart_item: CartItem) -> None:
        print(f"[ANALYTICS] Cart Add Event - User: {user_id}, Product: {cart_item.product_id}, Quantity: {cart_item.quantity}")
    
    def on_item_removed(self, user_id: int, product_id: int) -> None:
        print(f"[ANALYTICS] Cart Remove Event - User: {user_id}, Product: {product_id}")
    
    def on_quantity_updated(self, user_id: int, product_id: int, old_quantity: int, new_quantity: int) -> None:
        print(f"[ANALYTICS] Cart Update Event - User: {user_id}, Product: {product_id}, Old: {old_quantity}, New: {new_quantity}")
    
    def on_cart_cleared(self, user_id: int) -> None:
        print(f"[ANALYTICS] Cart Clear Event - User: {user_id}")