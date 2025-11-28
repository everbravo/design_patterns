from abc import ABC, abstractmethod
from typing import List, Optional
from src.models.product import Product

class ProductRepository(ABC):
    
    @abstractmethod
    def get_all(self) -> List[Product]:
        pass
    
    @abstractmethod
    def get_by_id(self, product_id: int) -> Optional[Product]:
        pass
    
    @abstractmethod
    def get_by_category(self, category: str) -> List[Product]:
        pass
    
    @abstractmethod
    def create(self, product: Product) -> Product:
        pass
    
    @abstractmethod
    def get_next_id(self) -> int:
        pass