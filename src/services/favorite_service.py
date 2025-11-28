from typing import List
from src.repositories.interfaces.favorite_repository import FavoriteRepository
from src.models.favorite import Favorite

class FavoriteService:
    
    def __init__(self, favorite_repository: FavoriteRepository):
        self.favorite_repository = favorite_repository
    
    def get_all_favorites(self) -> List[Favorite]:
        return self.favorite_repository.get_all()
    
    def add_favorite(self, user_id: int, product_id: int) -> Favorite:
        favorite = Favorite(user_id=user_id, product_id=product_id)
        return self.favorite_repository.create(favorite)
    
    def remove_favorite(self, user_id: int, product_id: int) -> bool:
        return self.favorite_repository.delete(user_id, product_id)