import unittest
from unittest.mock import Mock
from src.services.product_service import ProductService
from src.models.product import Product

class TestProductService(unittest.TestCase):
    
    def setUp(self):
        self.mock_repository = Mock()
        self.product_service = ProductService(self.mock_repository)
        self.test_product = Product(1, "Test Product", "electronics", 99.99)
    
    def test_get_all_products(self):
        # Setup mock
        expected_products = [self.test_product]
        self.mock_repository.get_all.return_value = expected_products
        
        # Execute
        result = self.product_service.get_all_products()
        
        # Verify
        self.assertEqual(result, expected_products)
        self.mock_repository.get_all.assert_called_once()
    
    def test_get_product_by_id_found(self):
        # Setup mock
        self.mock_repository.get_by_id.return_value = self.test_product
        
        # Execute
        result = self.product_service.get_product_by_id(1)
        
        # Verify
        self.assertEqual(result, self.test_product)
        self.mock_repository.get_by_id.assert_called_once_with(1)
    
    def test_get_product_by_id_not_found(self):
        # Setup mock
        self.mock_repository.get_by_id.return_value = None
        
        # Execute
        result = self.product_service.get_product_by_id(999)
        
        # Verify
        self.assertIsNone(result)
    
    def test_get_products_by_category(self):
        # Setup mock
        expected_products = [self.test_product]
        self.mock_repository.get_by_category.return_value = expected_products
        
        # Execute
        result = self.product_service.get_products_by_category("electronics")
        
        # Verify
        self.assertEqual(result, expected_products)
        self.mock_repository.get_by_category.assert_called_once_with("electronics")
    
    def test_create_product_success(self):
        # Setup mock
        self.mock_repository.get_next_id.return_value = 2
        self.mock_repository.create.return_value = self.test_product
        
        # Execute
        result = self.product_service.create_product("Test Product", "electronics", 99.99)
        
        # Verify
        self.assertIsNotNone(result)
        self.mock_repository.create.assert_called_once()
    
    def test_create_product_invalid_price(self):
        # Execute & Verify
        with self.assertRaises(ValueError):
            self.product_service.create_product("Test Product", "electronics", -10.0)
    
    def test_create_product_empty_name(self):
        # Execute & Verify
        with self.assertRaises(ValueError):
            self.product_service.create_product("", "electronics", 99.99)

if __name__ == '__main__':
    unittest.main()