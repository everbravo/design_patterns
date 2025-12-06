import json
import os
from typing import List, Optional
from src.repositories.interfaces.cart_repository import CartRepository
from src.models.cart_item import CartItem

class JsonCartRepository(CartRepository):
    
    def __init__(self, database_file: str):
        self.database_file = database_file
        self._ensure_database_exists()
    
    def _ensure_database_exists(self):
        if not os.path.exists(self.database_file):
            initial_data = {
                "products": [],
                "categories": [],
                "favorites": [],
                "carts": []
            }
            with open(self.database_file, 'w') as f:
                json.dump(initial_data, f, indent=4)
    
    def _load_data(self) -> dict:
        try:
            with open(self.database_file, 'r') as f:
                data = json.load(f)
                if 'carts' not in data:
                    data['carts'] = []
                return data
        except (FileNotFoundError, json.JSONDecodeError):
            return {"products": [], "categories": [], "favorites": [], "carts": []}
    
    def _save_data(self, data: dict):
        with open(self.database_file, 'w') as f:
            json.dump(data, f, indent=4)
    
    def _find_user_cart(self, data: dict, user_id: int) -> Optional[dict]:
        for cart in data['carts']:
            if cart['user_id'] == user_id:
                return cart
        return None
    
    def _create_user_cart(self, data: dict, user_id: int) -> dict:
        new_cart = {"user_id": user_id, "items": []}
        data['carts'].append(new_cart)
        return new_cart
    
    def get_cart_by_user_id(self, user_id: int) -> List[CartItem]:
        data = self._load_data()
        user_cart = self._find_user_cart(data, user_id)
        
        if not user_cart:
            return []
        
        cart_items = []
        for item_data in user_cart['items']:
            try:
                cart_item = CartItem.from_dict(item_data)
                cart_items.append(cart_item)
            except ValueError:
                continue  # Skip invalid items
        
        return cart_items
    
    def add_item(self, cart_item: CartItem) -> CartItem:
        data = self._load_data()
        user_cart = self._find_user_cart(data, cart_item.user_id)
        
        if not user_cart:
            user_cart = self._create_user_cart(data, cart_item.user_id)
        
        # Check if item already exists
        existing_item = None
        for item in user_cart['items']:
            if item['product_id'] == cart_item.product_id:
                existing_item = item
                break
        
        if existing_item:
            # Update quantity
            existing_item['quantity'] += cart_item.quantity
        else:
            # Add new item
            user_cart['items'].append(cart_item.to_dict())
        
        self._save_data(data)
        return cart_item
    
    def update_item_quantity(self, user_id: int, product_id: int, quantity: int) -> bool:
        if quantity <= 0:
            return self.remove_item(user_id, product_id)
        
        data = self._load_data()
        user_cart = self._find_user_cart(data, user_id)
        
        if not user_cart:
            return False
        
        for item in user_cart['items']:
            if item['product_id'] == product_id:
                item['quantity'] = quantity
                self._save_data(data)
                return True
        
        return False
    
    def remove_item(self, user_id: int, product_id: int) -> bool:
        data = self._load_data()
        user_cart = self._find_user_cart(data, user_id)
        
        if not user_cart:
            return False
        
        original_length = len(user_cart['items'])
        user_cart['items'] = [item for item in user_cart['items'] if item['product_id'] != product_id]
        
        if len(user_cart['items']) < original_length:
            self._save_data(data)
            return True
        
        return False
    
    def clear_cart(self, user_id: int) -> bool:
        data = self._load_data()
        user_cart = self._find_user_cart(data, user_id)
        
        if not user_cart:
            return False
        
        user_cart['items'] = []
        self._save_data(data)
        return True
    
    def get_item(self, user_id: int, product_id: int) -> Optional[CartItem]:
        data = self._load_data()
        user_cart = self._find_user_cart(data, user_id)
        
        if not user_cart:
            return None
        
        for item_data in user_cart['items']:
            if item_data['product_id'] == product_id:
                try:
                    return CartItem.from_dict(item_data)
                except ValueError:
                    return None
        
        return None