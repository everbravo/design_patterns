import unittest
from src.models.product import Product

class TestProduct(unittest.TestCase):
    
    def test_product_creation_valid(self):
        product = Product(1, "Test Product", "electronics", 99.99)
        self.assertEqual(product.id, 1)
        self.assertEqual(product.name, "Test Product")
        self.assertEqual(product.category, "electronics")
        self.assertEqual(product.price, 99.99)
    
    def test_product_negative_price_raises_error(self):
        with self.assertRaises(ValueError):
            Product(1, "Test Product", "electronics", -10.0)
    
    def test_product_empty_name_raises_error(self):
        with self.assertRaises(ValueError):
            Product(1, "", "electronics", 99.99)
    
    def test_product_empty_category_raises_error(self):
        with self.assertRaises(ValueError):
            Product(1, "Test Product", "", 99.99)
    
    def test_product_to_dict(self):
        product = Product(1, "Test Product", "electronics", 99.99)
        expected = {
            'id': 1,
            'name': 'Test Product',
            'category': 'electronics',
            'price': 99.99
        }
        self.assertEqual(product.to_dict(), expected)
    
    def test_product_from_dict_valid(self):
        data = {
            'id': 1,
            'name': 'Test Product',
            'category': 'electronics',
            'price': 99.99
        }
        product = Product.from_dict(data)
        self.assertEqual(product.id, 1)
        self.assertEqual(product.name, "Test Product")
    
    def test_product_from_dict_missing_field(self):
        data = {'id': 1, 'name': 'Test Product'}
        with self.assertRaises(ValueError):
            Product.from_dict(data)

if __name__ == '__main__':
    unittest.main()