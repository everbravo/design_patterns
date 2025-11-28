import json
from typing import List
from src.repositories.interfaces.favorite_repository import FavoriteRepository
from src.models.favorite import Favorite

class JsonFavoriteRepository(FavoriteRepository):
    
    def __init__(self, file_path: str):
        self.file_path = file_path
    
    def _load_data(self) -> dict:
        try:
            with open(self.file_path, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return {"products": [], "categories": [], "favorites": []}
    
    def _save_data(self, data: dict) -> None:
        with open(self.file_path, 'w') as file:
            json.dump(data, file, indent=4)
    
    def get_all(self) -> List[Favorite]:
        data = self._load_data()
        return [Favorite.from_dict(f) for f in data.get('favorites', [])]
    
    def create(self, favorite: Favorite) -> Favorite:
        data = self._load_data()
        favorites = data.get('favorites', [])
        favorites.append(favorite.to_dict())
        data['favorites'] = favorites
        self._save_data(data)
        return favorite
    
    def delete(self, user_id: int, product_id: int) -> bool:
        data = self._load_data()
        favorites = data.get('favorites', [])
        original_count = len(favorites)
        favorites = [f for f in favorites if not (f['user_id'] == user_id and f['product_id'] == product_id)]
        data['favorites'] = favorites
        self._save_data(data)
        return len(favorites) < original_count