from abc import ABC, abstractmethod
from typing import List
from src.models.cart_item import CartItem

class PricingStrategy(ABC):
    """Abstract base class for different pricing strategies"""
    
    @abstractmethod
    def calculate_item_total(self, cart_item: CartItem) -> float:
        """Calculate total price for a single cart item"""
        pass
    
    @abstractmethod
    def calculate_cart_total(self, items: List[CartItem]) -> float:
        """Calculate total price for all items in cart"""
        pass

class StandardPricingStrategy(PricingStrategy):
    """Standard pricing without any discounts"""
    
    def calculate_item_total(self, cart_item: CartItem) -> float:
        return cart_item.product_price * cart_item.quantity
    
    def calculate_cart_total(self, items: List[CartItem]) -> float:
        return sum(self.calculate_item_total(item) for item in items)

class DiscountPricingStrategy(PricingStrategy):
    """Pricing strategy with percentage discount"""
    
    def __init__(self, discount_percentage: float = 0.0):
        self.discount_percentage = max(0.0, min(100.0, discount_percentage))
    
    def calculate_item_total(self, cart_item: CartItem) -> float:
        base_total = cart_item.product_price * cart_item.quantity
        discount_amount = base_total * (self.discount_percentage / 100)
        return base_total - discount_amount
    
    def calculate_cart_total(self, items: List[CartItem]) -> float:
        return sum(self.calculate_item_total(item) for item in items)

class BulkDiscountPricingStrategy(PricingStrategy):
    """Pricing strategy with bulk discount (discount when quantity > threshold)"""
    
    def __init__(self, quantity_threshold: int = 5, discount_percentage: float = 10.0):
        self.quantity_threshold = quantity_threshold
        self.discount_percentage = max(0.0, min(100.0, discount_percentage))
    
    def calculate_item_total(self, cart_item: CartItem) -> float:
        base_total = cart_item.product_price * cart_item.quantity
        
        if cart_item.quantity >= self.quantity_threshold:
            discount_amount = base_total * (self.discount_percentage / 100)
            return base_total - discount_amount
        
        return base_total
    
    def calculate_cart_total(self, items: List[CartItem]) -> float:
        return sum(self.calculate_item_total(item) for item in items)