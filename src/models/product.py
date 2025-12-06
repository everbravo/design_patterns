from dataclasses import dataclass
from typing import Optional

@dataclass
class Product:
    id: int
    name: str
    category: str
    price: float
    
    def __post_init__(self):
        if self.price < 0:
            raise ValueError("Price cannot be negative")
        if not self.name.strip():
            raise ValueError("Name cannot be empty")
        if not self.category.strip():
            raise ValueError("Category cannot be empty")
    
    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'name': self.name,
            'category': self.category,
            'price': self.price
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Product':
        if not isinstance(data, dict):
            raise TypeError("Data must be a dictionary")
        
        try:
            return cls(
                id=data['id'],
                name=data['name'],
                category=data['category'],
                price=data['price']
            )
        except KeyError as e:
            raise ValueError(f"Missing required field: {e}")
        except (TypeError, ValueError) as e:
            raise ValueError(f"Invalid data format: {e}")