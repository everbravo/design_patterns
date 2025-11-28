import json
from typing import List, Optional
from src.repositories.interfaces.category_repository import CategoryRepository
from src.models.category import Category

class JsonCategoryRepository(CategoryRepository):
    
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
    
    def get_all(self) -> List[Category]:
        data = self._load_data()
        return [Category.from_dict(c) for c in data.get('categories', [])]
    
    def get_by_id(self, category_id: int) -> Optional[Category]:
        categories = self.get_all()
        return next((c for c in categories if c.id == category_id), None)
    
    def create(self, category: Category) -> Category:
        data = self._load_data()
        categories = data.get('categories', [])
        categories.append(category.to_dict())
        data['categories'] = categories
        self._save_data(data)
        return category
    
    def delete_by_name(self, name: str) -> bool:
        data = self._load_data()
        categories = data.get('categories', [])
        original_count = len(categories)
        categories = [c for c in categories if c['name'] != name]
        data['categories'] = categories
        self._save_data(data)
        return len(categories) < original_count
    
    def get_next_id(self) -> int:
        categories = self.get_all()
        return max([c.id for c in categories], default=0) + 1