import unittest
from src.models.category import Category

class TestCategory(unittest.TestCase):
    
    def test_category_creation_valid(self):
        category = Category(1, "Electronics")
        self.assertEqual(category.id, 1)
        self.assertEqual(category.name, "Electronics")
    
    def test_category_empty_name_raises_error(self):
        with self.assertRaises(ValueError):
            Category(1, "")
    
    def test_category_whitespace_name_raises_error(self):
        with self.assertRaises(ValueError):
            Category(1, "   ")
    
    def test_category_to_dict(self):
        category = Category(1, "Electronics")
        expected = {'id': 1, 'name': 'Electronics'}
        self.assertEqual(category.to_dict(), expected)
    
    def test_category_from_dict_valid(self):
        data = {'id': 1, 'name': 'Electronics'}
        category = Category.from_dict(data)
        self.assertEqual(category.id, 1)
        self.assertEqual(category.name, "Electronics")
    
    def test_category_from_dict_invalid_data(self):
        with self.assertRaises(TypeError):
            Category.from_dict("invalid")
    
    def test_category_from_dict_missing_field(self):
        data = {'id': 1}
        with self.assertRaises(ValueError):
            Category.from_dict(data)

if __name__ == '__main__':
    unittest.main()