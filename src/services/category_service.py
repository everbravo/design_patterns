from typing import List, Optional
from src.repositories.interfaces.category_repository import CategoryRepository
from src.models.category import Category

class CategoryService:
    
    def __init__(self, category_repository: CategoryRepository):
        self.category_repository = category_repository
    
    def get_all_categories(self) -> List[Category]:
        return self.category_repository.get_all()
    
    def get_category_by_id(self, category_id: int) -> Optional[Category]:
        return self.category_repository.get_by_id(category_id)
    
    def create_category(self, name: str) -> Category:
        category_id = self.category_repository.get_next_id()
        category = Category(id=category_id, name=name)
        return self.category_repository.create(category)
    
    def delete_category_by_name(self, name: str) -> bool:
        return self.category_repository.delete_by_name(name)