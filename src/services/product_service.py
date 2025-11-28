from typing import List, Optional
from src.repositories.interfaces.product_repository import ProductRepository
from src.models.product import Product

class ProductService:
    
    def __init__(self, product_repository: ProductRepository):
        self.product_repository = product_repository
    
    def get_all_products(self) -> List[Product]:
        return self.product_repository.get_all()
    
    def get_product_by_id(self, product_id: int) -> Optional[Product]:
        return self.product_repository.get_by_id(product_id)
    
    def get_products_by_category(self, category: str) -> List[Product]:
        return self.product_repository.get_by_category(category)
    
    def create_product(self, name: str, category: str, price: float) -> Product:
        product_id = self.product_repository.get_next_id()
        product = Product(id=product_id, name=name, category=category, price=price)
        return self.product_repository.create(product)