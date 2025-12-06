from typing import List, Optional
from src.repositories.interfaces.cart_repository import CartRepository
from src.services.product_service import ProductService
from src.strategies.pricing_strategy import PricingStrategy
from src.observers.cart_observer import CartObserver
from src.models.cart_item import CartItem

class CartService:
    """Service class for cart business logic"""
    
    def __init__(self, cart_repository: CartRepository, product_service: ProductService, pricing_strategy: PricingStrategy):
        self.cart_repository = cart_repository
        self.product_service = product_service
        self.pricing_strategy = pricing_strategy
        self.observers: List[CartObserver] = []
    
    def add_observer(self, observer: CartObserver) -> None:
        """Add an observer to the cart service"""
        if observer not in self.observers:
            self.observers.append(observer)
    
    def remove_observer(self, observer: CartObserver) -> None:
        """Remove an observer from the cart service"""
        if observer in self.observers:
            self.observers.remove(observer)
    
    def _notify_item_added(self, user_id: int, cart_item: CartItem) -> None:
        """Notify all observers that an item was added"""
        for observer in self.observers:
            observer.on_item_added(user_id, cart_item)
    
    def _notify_item_removed(self, user_id: int, product_id: int) -> None:
        """Notify all observers that an item was removed"""
        for observer in self.observers:
            observer.on_item_removed(user_id, product_id)
    
    def _notify_quantity_updated(self, user_id: int, product_id: int, old_quantity: int, new_quantity: int) -> None:
        """Notify all observers that quantity was updated"""
        for observer in self.observers:
            observer.on_quantity_updated(user_id, product_id, old_quantity, new_quantity)
    
    def _notify_cart_cleared(self, user_id: int) -> None:
        """Notify all observers that cart was cleared"""
        for observer in self.observers:
            observer.on_cart_cleared(user_id)
    
    def add_item(self, user_id: int, product_id: int, quantity: int) -> Optional[CartItem]:
        """Add an item to the cart"""
        if quantity <= 0:
            raise ValueError("Quantity must be greater than 0")
        
        # Validate product exists
        product = self.product_service.get_product_by_id(product_id)
        if not product:
            raise ValueError("Product not found")
        
        # Create cart item
        cart_item = CartItem(
            user_id=user_id,
            product_id=product_id,
            product_name=product.name,
            product_price=product.price,
            quantity=quantity
        )
        
        # Add to repository
        result = self.cart_repository.add_item(cart_item)
        
        # Notify observers
        self._notify_item_added(user_id, cart_item)
        
        return result
    
    def remove_item(self, user_id: int, product_id: int) -> bool:
        """Remove an item from the cart"""
        result = self.cart_repository.remove_item(user_id, product_id)
        
        if result:
            self._notify_item_removed(user_id, product_id)
        
        return result
    
    def update_item_quantity(self, user_id: int, product_id: int, quantity: int) -> bool:
        """Update the quantity of an item in the cart"""
        if quantity <= 0:
            return self.remove_item(user_id, product_id)
        
        # Get current quantity for notification
        current_item = self.cart_repository.get_item(user_id, product_id)
        old_quantity = current_item.quantity if current_item else 0
        
        result = self.cart_repository.update_item_quantity(user_id, product_id, quantity)
        
        if result:
            self._notify_quantity_updated(user_id, product_id, old_quantity, quantity)
        
        return result
    
    def get_cart_items(self, user_id: int) -> List[CartItem]:
        """Get all items in the user's cart"""
        return self.cart_repository.get_cart_by_user_id(user_id)
    
    def get_cart_item(self, user_id: int, product_id: int) -> Optional[CartItem]:
        """Get a specific item from the cart"""
        return self.cart_repository.get_item(user_id, product_id)
    
    def clear_cart(self, user_id: int) -> bool:
        """Clear all items from the cart"""
        result = self.cart_repository.clear_cart(user_id)
        
        if result:
            self._notify_cart_cleared(user_id)
        
        return result
    
    def get_cart_summary(self, user_id: int) -> dict:
        """Get cart summary with totals"""
        items = self.get_cart_items(user_id)
        
        total_items = sum(item.quantity for item in items)
        total_price = self.pricing_strategy.calculate_cart_total(items)
        
        return {
            'items': [item.to_dict() for item in items],
            'total_items': total_items,
            'total_price': round(total_price, 2),
            'item_count': len(items)
        }
    
    def get_cart_total(self, user_id: int) -> float:
        """Get the total price of items in the cart"""
        items = self.get_cart_items(user_id)
        return self.pricing_strategy.calculate_cart_total(items)