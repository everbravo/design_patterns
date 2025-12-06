from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.services.cart_service import CartService

class CartCommand(ABC):
    """Abstract base class for cart commands"""
    
    @abstractmethod
    def execute(self) -> bool:
        """Execute the command"""
        pass
    
    @abstractmethod
    def undo(self) -> bool:
        """Undo the command"""
        pass

class AddItemCommand(CartCommand):
    """Command to add an item to the cart"""
    
    def __init__(self, cart_service: 'CartService', user_id: int, product_id: int, quantity: int):
        self.cart_service = cart_service
        self.user_id = user_id
        self.product_id = product_id
        self.quantity = quantity
        self.executed = False
    
    def execute(self) -> bool:
        try:
            result = self.cart_service.add_item(self.user_id, self.product_id, self.quantity)
            self.executed = True
            return result is not None
        except Exception:
            return False
    
    def undo(self) -> bool:
        if not self.executed:
            return False
        try:
            return self.cart_service.remove_item(self.user_id, self.product_id)
        except Exception:
            return False

class RemoveItemCommand(CartCommand):
    """Command to remove an item from the cart"""
    
    def __init__(self, cart_service: 'CartService', user_id: int, product_id: int):
        self.cart_service = cart_service
        self.user_id = user_id
        self.product_id = product_id
        self.backup_item = None
        self.executed = False
    
    def execute(self) -> bool:
        try:
            # Backup the item before removing
            self.backup_item = self.cart_service.get_cart_item(self.user_id, self.product_id)
            result = self.cart_service.remove_item(self.user_id, self.product_id)
            self.executed = True
            return result
        except Exception:
            return False
    
    def undo(self) -> bool:
        if not self.executed or not self.backup_item:
            return False
        try:
            return self.cart_service.add_item(
                self.user_id, 
                self.backup_item.product_id, 
                self.backup_item.quantity
            ) is not None
        except Exception:
            return False

class UpdateQuantityCommand(CartCommand):
    """Command to update item quantity in the cart"""
    
    def __init__(self, cart_service: 'CartService', user_id: int, product_id: int, new_quantity: int):
        self.cart_service = cart_service
        self.user_id = user_id
        self.product_id = product_id
        self.new_quantity = new_quantity
        self.old_quantity = None
        self.executed = False
    
    def execute(self) -> bool:
        try:
            # Backup old quantity
            current_item = self.cart_service.get_cart_item(self.user_id, self.product_id)
            if current_item:
                self.old_quantity = current_item.quantity
            
            result = self.cart_service.update_item_quantity(self.user_id, self.product_id, self.new_quantity)
            self.executed = True
            return result
        except Exception:
            return False
    
    def undo(self) -> bool:
        if not self.executed or self.old_quantity is None:
            return False
        try:
            return self.cart_service.update_item_quantity(self.user_id, self.product_id, self.old_quantity)
        except Exception:
            return False

class ClearCartCommand(CartCommand):
    """Command to clear the entire cart"""
    
    def __init__(self, cart_service: 'CartService', user_id: int):
        self.cart_service = cart_service
        self.user_id = user_id
        self.backup_items = []
        self.executed = False
    
    def execute(self) -> bool:
        try:
            # Backup all items before clearing
            self.backup_items = self.cart_service.get_cart_items(self.user_id)
            result = self.cart_service.clear_cart(self.user_id)
            self.executed = True
            return result
        except Exception:
            return False
    
    def undo(self) -> bool:
        if not self.executed:
            return False
        try:
            # Restore all backed up items
            for item in self.backup_items:
                self.cart_service.add_item(self.user_id, item.product_id, item.quantity)
            return True
        except Exception:
            return False