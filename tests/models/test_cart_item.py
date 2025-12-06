import unittest
from datetime import datetime
from src.models.cart_item import CartItem

class TestCartItem(unittest.TestCase):
    
    def test_cart_item_creation_valid(self):
        cart_item = CartItem(1, 1, "Test Product", 10.0, 2)
        self.assertEqual(cart_item.user_id, 1)
        self.assertEqual(cart_item.product_id, 1)
        self.assertEqual(cart_item.product_name, "Test Product")
        self.assertEqual(cart_item.product_price, 10.0)
        self.assertEqual(cart_item.quantity, 2)
        self.assertIsInstance(cart_item.added_at, datetime)
    
    def test_cart_item_zero_quantity_raises_error(self):
        with self.assertRaises(ValueError):
            CartItem(1, 1, "Test Product", 10.0, 0)
    
    def test_cart_item_negative_quantity_raises_error(self):
        with self.assertRaises(ValueError):
            CartItem(1, 1, "Test Product", 10.0, -1)
    
    def test_cart_item_negative_price_raises_error(self):
        with self.assertRaises(ValueError):
            CartItem(1, 1, "Test Product", -10.0, 2)
    
    def test_cart_item_empty_name_raises_error(self):
        with self.assertRaises(ValueError):
            CartItem(1, 1, "", 10.0, 2)
    
    def test_cart_item_get_total_price(self):
        cart_item = CartItem(1, 1, "Test Product", 10.0, 3)
        self.assertEqual(cart_item.get_total_price(), 30.0)
    
    def test_cart_item_to_dict(self):
        cart_item = CartItem(1, 1, "Test Product", 10.0, 2)
        result = cart_item.to_dict()
        self.assertEqual(result['user_id'], 1)
        self.assertEqual(result['product_id'], 1)
        self.assertEqual(result['total_price'], 20.0)
        self.assertIn('added_at', result)
    
    def test_cart_item_from_dict_valid(self):
        data = {
            'user_id': 1,
            'product_id': 1,
            'product_name': 'Test Product',
            'product_price': 10.0,
            'quantity': 2,
            'added_at': '2024-01-01T10:00:00'
        }
        cart_item = CartItem.from_dict(data)
        self.assertEqual(cart_item.user_id, 1)
        self.assertEqual(cart_item.quantity, 2)
    
    def test_cart_item_from_dict_missing_field(self):
        data = {'user_id': 1, 'product_id': 1}
        with self.assertRaises(ValueError):
            CartItem.from_dict(data)

if __name__ == '__main__':
    unittest.main()