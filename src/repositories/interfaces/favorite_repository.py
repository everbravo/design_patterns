from abc import ABC, abstractmethod
from typing import List
from src.models.favorite import Favorite

class FavoriteRepository(ABC):
    
    @abstractmethod
    def get_all(self) -> List[Favorite]:
        pass
    
    @abstractmethod
    def create(self, favorite: Favorite) -> Favorite:
        pass
    
    @abstractmethod
    def delete(self, user_id: int, product_id: int) -> bool:
        pass