from abc import ABC, abstractmethod
from typing import List, Optional
from src.models.category import Category

class CategoryRepository(ABC):
    
    @abstractmethod
    def get_all(self) -> List[Category]:
        pass
    
    @abstractmethod
    def get_by_id(self, category_id: int) -> Optional[Category]:
        pass
    
    @abstractmethod
    def create(self, category: Category) -> Category:
        pass
    
    @abstractmethod
    def delete_by_name(self, name: str) -> bool:
        pass
    
    @abstractmethod
    def get_next_id(self) -> int:
        pass