from dataclasses import dataclass

@dataclass
class Favorite:
    user_id: int
    product_id: int
    
    def to_dict(self) -> dict:
        return {
            'user_id': self.user_id,
            'product_id': self.product_id
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Favorite':
        return cls(
            user_id=data['user_id'],
            product_id=data['product_id']
        )