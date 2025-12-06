import unittest
from src.strategies.pricing_strategy import StandardPricingStrategy, DiscountPricingStrategy, BulkDiscountPricingStrategy
from src.models.cart_item import CartItem

class TestPricingStrategies(unittest.TestCase):
    
    def setUp(self):
        self.cart_item1 = CartItem(1, 1, "Product 1", 10.0, 2)
        self.cart_item2 = CartItem(1, 2, "Product 2", 20.0, 3)
        self.cart_items = [self.cart_item1, self.cart_item2]
    
    def test_standard_pricing_item_total(self):
        strategy = StandardPricingStrategy()
        total = strategy.calculate_item_total(self.cart_item1)
        self.assertEqual(total, 20.0)  # 10.0 * 2
    
    def test_standard_pricing_cart_total(self):
        strategy = StandardPricingStrategy()
        total = strategy.calculate_cart_total(self.cart_items)
        self.assertEqual(total, 80.0)  # (10*2) + (20*3)
    
    def test_discount_pricing_10_percent(self):
        strategy = DiscountPricingStrategy(10.0)
        total = strategy.calculate_item_total(self.cart_item1)
        self.assertEqual(total, 18.0)  # 20.0 - (20.0 * 0.1)
    
    def test_discount_pricing_cart_total(self):
        strategy = DiscountPricingStrategy(10.0)
        total = strategy.calculate_cart_total(self.cart_items)
        self.assertEqual(total, 72.0)  # 80.0 - (80.0 * 0.1)
    
    def test_discount_pricing_invalid_percentage(self):
        strategy = DiscountPricingStrategy(150.0)  # Should be clamped to 100
        self.assertEqual(strategy.discount_percentage, 100.0)
        
        strategy = DiscountPricingStrategy(-10.0)  # Should be clamped to 0
        self.assertEqual(strategy.discount_percentage, 0.0)
    
    def test_bulk_discount_below_threshold(self):
        strategy = BulkDiscountPricingStrategy(5, 10.0)
        total = strategy.calculate_item_total(self.cart_item1)  # quantity = 2
        self.assertEqual(total, 20.0)  # No discount
    
    def test_bulk_discount_above_threshold(self):
        bulk_item = CartItem(1, 1, "Bulk Product", 10.0, 6)
        strategy = BulkDiscountPricingStrategy(5, 10.0)
        total = strategy.calculate_item_total(bulk_item)
        self.assertEqual(total, 54.0)  # 60.0 - (60.0 * 0.1)
    
    def test_bulk_discount_cart_total_mixed(self):
        bulk_item = CartItem(1, 3, "Bulk Product", 10.0, 6)
        items = [self.cart_item1, bulk_item]  # One below, one above threshold
        strategy = BulkDiscountPricingStrategy(5, 10.0)
        total = strategy.calculate_cart_total(items)
        self.assertEqual(total, 74.0)  # 20.0 + 54.0

if __name__ == '__main__':
    unittest.main()