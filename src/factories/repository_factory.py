from src.repositories.interfaces.product_repository import ProductRepository
from src.repositories.interfaces.category_repository import CategoryRepository
from src.repositories.interfaces.favorite_repository import FavoriteRepository
from src.repositories.interfaces.cart_repository import CartRepository
from src.repositories.implementations.json_product_repository import JsonProductRepository
from src.repositories.implementations.json_category_repository import JsonCategoryRepository
from src.repositories.implementations.json_favorite_repository import JsonFavoriteRepository
from src.repositories.implementations.json_cart_repository import JsonCartRepository

class RepositoryFactory:
    
    @staticmethod
    def create_product_repository(file_path: str = 'db.json') -> ProductRepository:
        return JsonProductRepository(file_path)
    
    @staticmethod
    def create_category_repository(file_path: str = 'db.json') -> CategoryRepository:
        return JsonCategoryRepository(file_path)
    
    @staticmethod
    def create_favorite_repository(file_path: str = 'db.json') -> FavoriteRepository:
        return JsonFavoriteRepository(file_path)
    
    @staticmethod
    def create_cart_repository(file_path: str = 'db.json') -> CartRepository:
        return JsonCartRepository(file_path)