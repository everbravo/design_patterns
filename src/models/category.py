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
        return cls(
            id=data['id'],
            name=data['name']
        )