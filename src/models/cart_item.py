from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class CartItem:
    user_id: int
    product_id: int
    product_name: str
    product_price: float
    quantity: int
    added_at: Optional[datetime] = None
    
    def __post_init__(self):
        if self.quantity <= 0:
            raise ValueError("Quantity must be greater than 0")
        if self.product_price < 0:
            raise ValueError("Product price cannot be negative")
        if not self.product_name.strip():
            raise ValueError("Product name cannot be empty")
        if self.added_at is None:
            self.added_at = datetime.now()
    
    def get_total_price(self) -> float:
        return self.product_price * self.quantity
    
    def to_dict(self) -> dict:
        return {
            'user_id': self.user_id,
            'product_id': self.product_id,
            'product_name': self.product_name,
            'product_price': self.product_price,
            'quantity': self.quantity,
            'added_at': self.added_at.isoformat() if self.added_at else None,
            'total_price': self.get_total_price()
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'CartItem':
        if not isinstance(data, dict):
            raise TypeError("Data must be a dictionary")
        
        try:
            added_at = None
            if 'added_at' in data and data['added_at']:
                added_at = datetime.fromisoformat(data['added_at'])
            
            return cls(
                user_id=data['user_id'],
                product_id=data['product_id'],
                product_name=data['product_name'],
                product_price=data['product_price'],
                quantity=data['quantity'],
                added_at=added_at
            )
        except KeyError as e:
            raise ValueError(f"Missing required field: {e}")
        except (TypeError, ValueError) as e:
            raise ValueError(f"Invalid data format: {e}")