import unittest
import tempfile
import json
import os
from src.repositories.implementations.json_cart_repository import JsonCartRepository
from src.models.cart_item import CartItem

class TestJsonCartRepository(unittest.TestCase):
    
    def setUp(self):
        # Create temporary file for testing
        self.temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json')
        self.temp_file_path = self.temp_file.name
        
        # Initialize with test data
        initial_data = {
            "products": [],
            "categories": [],
            "favorites": [],
            "carts": []
        }
        json.dump(initial_data, self.temp_file)
        self.temp_file.close()
        
        self.repository = JsonCartRepository(self.temp_file_path)
        self.test_cart_item = CartItem(1, 1, "Test Product", 10.0, 2)
    
    def tearDown(self):
        # Clean up temporary file
        if os.path.exists(self.temp_file_path):
            os.unlink(self.temp_file_path)
    
    def test_get_cart_by_user_id_empty(self):
        result = self.repository.get_cart_by_user_id(1)
        self.assertEqual(result, [])
    
    def test_add_item_new_user(self):
        result = self.repository.add_item(self.test_cart_item)
        self.assertIsNotNone(result)
        
        # Verify item was added
        cart_items = self.repository.get_cart_by_user_id(1)
        self.assertEqual(len(cart_items), 1)
        self.assertEqual(cart_items[0].product_id, 1)
    
    def test_add_item_existing_product(self):
        # Add item first time
        self.repository.add_item(self.test_cart_item)
        
        # Add same product again
        another_item = CartItem(1, 1, "Test Product", 10.0, 3)
        self.repository.add_item(another_item)
        
        # Verify quantity was updated, not new item created
        cart_items = self.repository.get_cart_by_user_id(1)
        self.assertEqual(len(cart_items), 1)
        self.assertEqual(cart_items[0].quantity, 5)  # 2 + 3
    
    def test_update_item_quantity_success(self):
        # Add item first
        self.repository.add_item(self.test_cart_item)
        
        # Update quantity
        result = self.repository.update_item_quantity(1, 1, 5)
        self.assertTrue(result)
        
        # Verify update
        cart_items = self.repository.get_cart_by_user_id(1)
        self.assertEqual(cart_items[0].quantity, 5)
    
    def test_update_item_quantity_zero_removes_item(self):
        # Add item first
        self.repository.add_item(self.test_cart_item)
        
        # Update quantity to 0
        result = self.repository.update_item_quantity(1, 1, 0)
        self.assertTrue(result)
        
        # Verify item was removed
        cart_items = self.repository.get_cart_by_user_id(1)
        self.assertEqual(len(cart_items), 0)
    
    def test_remove_item_success(self):
        # Add item first
        self.repository.add_item(self.test_cart_item)
        
        # Remove item
        result = self.repository.remove_item(1, 1)
        self.assertTrue(result)
        
        # Verify removal
        cart_items = self.repository.get_cart_by_user_id(1)
        self.assertEqual(len(cart_items), 0)
    
    def test_remove_item_not_found(self):
        result = self.repository.remove_item(1, 999)
        self.assertFalse(result)
    
    def test_clear_cart_success(self):
        # Add multiple items
        self.repository.add_item(self.test_cart_item)
        item2 = CartItem(1, 2, "Product 2", 20.0, 1)
        self.repository.add_item(item2)
        
        # Clear cart
        result = self.repository.clear_cart(1)
        self.assertTrue(result)
        
        # Verify cart is empty
        cart_items = self.repository.get_cart_by_user_id(1)
        self.assertEqual(len(cart_items), 0)
    
    def test_get_item_found(self):
        # Add item first
        self.repository.add_item(self.test_cart_item)
        
        # Get specific item
        result = self.repository.get_item(1, 1)
        self.assertIsNotNone(result)
        self.assertEqual(result.product_id, 1)
    
    def test_get_item_not_found(self):
        result = self.repository.get_item(1, 999)
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()