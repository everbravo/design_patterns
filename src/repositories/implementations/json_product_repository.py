import json
from typing import List, Optional
from src.repositories.interfaces.product_repository import ProductRepository
from src.models.product import Product

class JsonProductRepository(ProductRepository):
    
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
    
    def get_all(self) -> List[Product]:
        data = self._load_data()
        return [Product.from_dict(p) for p in data.get('products', [])]
    
    def get_by_id(self, product_id: int) -> Optional[Product]:
        products = self.get_all()
        return next((p for p in products if p.id == product_id), None)
    
    def get_by_category(self, category: str) -> List[Product]:
        products = self.get_all()
        return [p for p in products if p.category.lower() == category.lower()]
    
    def create(self, product: Product) -> Product:
        data = self._load_data()
        products = data.get('products', [])
        products.append(product.to_dict())
        data['products'] = products
        self._save_data(data)
        return product
    
    def get_next_id(self) -> int:
        products = self.get_all()
        return max([p.id for p in products], default=0) + 1