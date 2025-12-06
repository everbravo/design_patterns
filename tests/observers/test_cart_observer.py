import unittest
from unittest.mock import patch
from io import StringIO
from src.observers.cart_observer import InventoryObserver, AnalyticsObserver
from src.models.cart_item import CartItem

class TestCartObservers(unittest.TestCase):
    
    def setUp(self):
        self.inventory_observer = InventoryObserver()
        self.analytics_observer = AnalyticsObserver()
        self.test_cart_item = CartItem(1, 1, "Test Product", 10.0, 2)
    
    @patch('sys.stdout', new_callable=StringIO)
    def test_inventory_observer_item_added(self, mock_stdout):
        self.inventory_observer.on_item_added(1, self.test_cart_item)
        output = mock_stdout.getvalue()
        self.assertIn("[INVENTORY]", output)
        self.assertIn("User 1 added 2x Test Product to cart", output)
    
    @patch('sys.stdout', new_callable=StringIO)
    def test_inventory_observer_item_removed(self, mock_stdout):
        self.inventory_observer.on_item_removed(1, 1)
        output = mock_stdout.getvalue()
        self.assertIn("[INVENTORY]", output)
        self.assertIn("User 1 removed product 1 from cart", output)
    
    @patch('sys.stdout', new_callable=StringIO)
    def test_inventory_observer_quantity_updated_increased(self, mock_stdout):
        self.inventory_observer.on_quantity_updated(1, 1, 2, 5)
        output = mock_stdout.getvalue()
        self.assertIn("[INVENTORY]", output)
        self.assertIn("User 1 increased product 1 quantity by 3", output)
    
    @patch('sys.stdout', new_callable=StringIO)
    def test_inventory_observer_quantity_updated_decreased(self, mock_stdout):
        self.inventory_observer.on_quantity_updated(1, 1, 5, 2)
        output = mock_stdout.getvalue()
        self.assertIn("[INVENTORY]", output)
        self.assertIn("User 1 decreased product 1 quantity by 3", output)
    
    @patch('sys.stdout', new_callable=StringIO)
    def test_inventory_observer_cart_cleared(self, mock_stdout):
        self.inventory_observer.on_cart_cleared(1)
        output = mock_stdout.getvalue()
        self.assertIn("[INVENTORY]", output)
        self.assertIn("User 1 cleared their entire cart", output)
    
    @patch('sys.stdout', new_callable=StringIO)
    def test_analytics_observer_item_added(self, mock_stdout):
        self.analytics_observer.on_item_added(1, self.test_cart_item)
        output = mock_stdout.getvalue()
        self.assertIn("[ANALYTICS]", output)
        self.assertIn("Cart Add Event - User: 1, Product: 1, Quantity: 2", output)
    
    @patch('sys.stdout', new_callable=StringIO)
    def test_analytics_observer_item_removed(self, mock_stdout):
        self.analytics_observer.on_item_removed(1, 1)
        output = mock_stdout.getvalue()
        self.assertIn("[ANALYTICS]", output)
        self.assertIn("Cart Remove Event - User: 1, Product: 1", output)
    
    @patch('sys.stdout', new_callable=StringIO)
    def test_analytics_observer_quantity_updated(self, mock_stdout):
        self.analytics_observer.on_quantity_updated(1, 1, 2, 5)
        output = mock_stdout.getvalue()
        self.assertIn("[ANALYTICS]", output)
        self.assertIn("Cart Update Event - User: 1, Product: 1, Old: 2, New: 5", output)
    
    @patch('sys.stdout', new_callable=StringIO)
    def test_analytics_observer_cart_cleared(self, mock_stdout):
        self.analytics_observer.on_cart_cleared(1)
        output = mock_stdout.getvalue()
        self.assertIn("[ANALYTICS]", output)
        self.assertIn("Cart Clear Event - User: 1", output)

if __name__ == '__main__':
    unittest.main()