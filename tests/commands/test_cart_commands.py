import unittest
from unittest.mock import Mock
from src.commands.cart_commands import AddItemCommand, RemoveItemCommand, UpdateQuantityCommand, ClearCartCommand
from src.models.cart_item import CartItem

class TestCartCommands(unittest.TestCase):
    
    def setUp(self):
        self.mock_cart_service = Mock()
        self.test_cart_item = CartItem(1, 1, "Test Product", 10.0, 2)
    
    def test_add_item_command_execute_success(self):
        # Setup
        self.mock_cart_service.add_item.return_value = self.test_cart_item
        command = AddItemCommand(self.mock_cart_service, 1, 1, 2)
        
        # Execute
        result = command.execute()
        
        # Verify
        self.assertTrue(result)
        self.mock_cart_service.add_item.assert_called_once_with(1, 1, 2)
    
    def test_add_item_command_execute_failure(self):
        # Setup
        self.mock_cart_service.add_item.side_effect = Exception("Error")
        command = AddItemCommand(self.mock_cart_service, 1, 1, 2)
        
        # Execute
        result = command.execute()
        
        # Verify
        self.assertFalse(result)
    
    def test_add_item_command_undo_success(self):
        # Setup
        self.mock_cart_service.add_item.return_value = self.test_cart_item
        self.mock_cart_service.remove_item.return_value = True
        command = AddItemCommand(self.mock_cart_service, 1, 1, 2)
        
        # Execute and undo
        command.execute()
        result = command.undo()
        
        # Verify
        self.assertTrue(result)
        self.mock_cart_service.remove_item.assert_called_once_with(1, 1)
    
    def test_add_item_command_undo_not_executed(self):
        # Setup
        command = AddItemCommand(self.mock_cart_service, 1, 1, 2)
        
        # Execute undo without execute
        result = command.undo()
        
        # Verify
        self.assertFalse(result)
    
    def test_remove_item_command_execute_success(self):
        # Setup
        self.mock_cart_service.get_cart_item.return_value = self.test_cart_item
        self.mock_cart_service.remove_item.return_value = True
        command = RemoveItemCommand(self.mock_cart_service, 1, 1)
        
        # Execute
        result = command.execute()
        
        # Verify
        self.assertTrue(result)
        self.mock_cart_service.remove_item.assert_called_once_with(1, 1)
    
    def test_remove_item_command_undo_success(self):
        # Setup
        self.mock_cart_service.get_cart_item.return_value = self.test_cart_item
        self.mock_cart_service.remove_item.return_value = True
        self.mock_cart_service.add_item.return_value = self.test_cart_item
        command = RemoveItemCommand(self.mock_cart_service, 1, 1)
        
        # Execute and undo
        command.execute()
        result = command.undo()
        
        # Verify
        self.assertTrue(result)
        self.mock_cart_service.add_item.assert_called_once_with(1, 1, 2)
    
    def test_update_quantity_command_execute_success(self):
        # Setup
        self.mock_cart_service.get_cart_item.return_value = self.test_cart_item
        self.mock_cart_service.update_item_quantity.return_value = True
        command = UpdateQuantityCommand(self.mock_cart_service, 1, 1, 5)
        
        # Execute
        result = command.execute()
        
        # Verify
        self.assertTrue(result)
        self.mock_cart_service.update_item_quantity.assert_called_once_with(1, 1, 5)
    
    def test_update_quantity_command_undo_success(self):
        # Setup
        self.mock_cart_service.get_cart_item.return_value = self.test_cart_item
        self.mock_cart_service.update_item_quantity.return_value = True
        command = UpdateQuantityCommand(self.mock_cart_service, 1, 1, 5)
        
        # Execute and undo
        command.execute()
        result = command.undo()
        
        # Verify
        self.assertTrue(result)
        # Should be called twice: once for execute, once for undo
        self.assertEqual(self.mock_cart_service.update_item_quantity.call_count, 2)
    
    def test_clear_cart_command_execute_success(self):
        # Setup
        self.mock_cart_service.get_cart_items.return_value = [self.test_cart_item]
        self.mock_cart_service.clear_cart.return_value = True
        command = ClearCartCommand(self.mock_cart_service, 1)
        
        # Execute
        result = command.execute()
        
        # Verify
        self.assertTrue(result)
        self.mock_cart_service.clear_cart.assert_called_once_with(1)
    
    def test_clear_cart_command_undo_success(self):
        # Setup
        self.mock_cart_service.get_cart_items.return_value = [self.test_cart_item]
        self.mock_cart_service.clear_cart.return_value = True
        self.mock_cart_service.add_item.return_value = self.test_cart_item
        command = ClearCartCommand(self.mock_cart_service, 1)
        
        # Execute and undo
        command.execute()
        result = command.undo()
        
        # Verify
        self.assertTrue(result)
        self.mock_cart_service.add_item.assert_called_once_with(1, 1, 2)

if __name__ == '__main__':
    unittest.main()