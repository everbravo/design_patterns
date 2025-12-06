from dataclasses import dataclass

@dataclass
class Category:
    id: int
    name: str
    
    def __post_init__(self):
        if not self.name.strip():
            raise ValueError("Category name cannot be empty")
    
    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'name': self.name
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Category':
        if not isinstance(data, dict):
            raise TypeError("Data must be a dictionary")
        
        try:
            return cls(
                id=data['id'],
                name=data['name']
            )
        except KeyError as e:
            raise ValueError(f"Missing required field: {e}")
        except (TypeError, ValueError) as e:
            raise ValueError(f"Invalid data format: {e}")