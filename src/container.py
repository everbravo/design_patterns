from src.factories.repository_factory import RepositoryFactory
from src.strategies.auth_strategy import SimpleAuthStrategy
from src.services.product_service import ProductService
from src.services.category_service import CategoryService
from src.services.favorite_service import FavoriteService
from src.services.auth_service import AuthService
from src.controllers.product_controller import ProductController
from src.controllers.category_controller import CategoryController
from src.controllers.favorite_controller import FavoriteController
from src.controllers.auth_controller import AuthController
from src.config.config import Config

class Container:
    def __init__(self):
        self._instances = {}
        self._setup_dependencies()
    
    def _setup_dependencies(self):
        self._instances['product_repository'] = RepositoryFactory.create_product_repository(Config.DATABASE_FILE)
        self._instances['category_repository'] = RepositoryFactory.create_category_repository(Config.DATABASE_FILE)
        self._instances['favorite_repository'] = RepositoryFactory.create_favorite_repository(Config.DATABASE_FILE)
        
        self._instances['auth_strategy'] = SimpleAuthStrategy()
        
        self._instances['product_service'] = ProductService(self._instances['product_repository'])
        self._instances['category_service'] = CategoryService(self._instances['category_repository'])
        self._instances['favorite_service'] = FavoriteService(self._instances['favorite_repository'])
        self._instances['auth_service'] = AuthService(self._instances['auth_strategy'])
        
        self._instances['product_controller_args'] = (self._instances['product_service'], self._instances['auth_service'])
        self._instances['category_controller_args'] = (self._instances['category_service'], self._instances['auth_service'])
        self._instances['favorite_controller_args'] = (self._instances['favorite_service'], self._instances['auth_service'])
        self._instances['auth_controller_args'] = (self._instances['auth_service'],)
    
    def get(self, name: str):
        if name == 'auth_controller':
            return AuthController
        elif name == 'product_controller':
            return ProductController
        elif name == 'category_controller':
            return CategoryController
        elif name == 'favorite_controller':
            return FavoriteController
        else:
            return self._instances.get(name)