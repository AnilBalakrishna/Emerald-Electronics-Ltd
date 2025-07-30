import unittest
import os
import json
import tempfile
import shutil
from data_manager import DataManager

class TestDataManager(unittest.TestCase):
    
    def setUp(self):
        """Set up test environment with temporary directory"""
        self.test_dir = tempfile.mkdtemp()
        self.original_dir = os.getcwd()
        os.chdir(self.test_dir)
        
        self.data_manager = DataManager()
    
    def tearDown(self):
        """Clean up test environment"""
        os.chdir(self.original_dir)
        shutil.rmtree(self.test_dir)
    
    def test_files_creation(self):
        """Test that JSON files are created"""
        self.assertTrue(os.path.exists('products.json'))
        self.assertTrue(os.path.exists('customers.json'))
    
    def test_create_product(self):
        """Test creating a new product"""
        product = self.data_manager.create_product("Test Product", 99.99, 10)
        
        self.assertEqual(product['name'], "Test Product")
        self.assertEqual(product['price'], 99.99)
        self.assertEqual(product['stock'], 10)
        self.assertEqual(product['id'], 1)
    
    def test_get_all_products(self):
        """Test getting all products"""
        # Initially empty
        products = self.data_manager.get_all_products()
        self.assertEqual(len(products), 0)
        
        # Add products
        self.data_manager.create_product("Product 1", 10.00, 5)
        self.data_manager.create_product("Product 2", 20.00, 3)
        
        products = self.data_manager.get_all_products()
        self.assertEqual(len(products), 2)
    
    def test_get_product(self):
        """Test getting a specific product"""
        # Create a product
        created_product = self.data_manager.create_product("Test Product", 99.99, 10)
        
        # Get the product
        product = self.data_manager.get_product(created_product['id'])
        self.assertIsNotNone(product)
        self.assertEqual(product['name'], "Test Product")
        
        # Non-existent product
        product = self.data_manager.get_product(999)
        self.assertIsNone(product)
    
    def test_update_product(self):
        """Test updating a product"""
        # Create a product
        created_product = self.data_manager.create_product("Test Product", 99.99, 10)
        
        # Update the product
        updates = {"name": "Updated Product", "price": 149.99}
        updated_product = self.data_manager.update_product(created_product['id'], updates)
        
        self.assertIsNotNone(updated_product)
        self.assertEqual(updated_product['name'], "Updated Product")
        self.assertEqual(updated_product['price'], 149.99)
        self.assertEqual(updated_product['stock'], 10)  # Unchanged
        
        # Non-existent product
        result = self.data_manager.update_product(999, updates)
        self.assertIsNone(result)
    
    def test_delete_product(self):
        """Test deleting a product"""
        # Create a product
        created_product = self.data_manager.create_product("Test Product", 99.99, 10)
        
        # Delete the product
        result = self.data_manager.delete_product(created_product['id'])
        self.assertTrue(result)
        
        # Verify deletion
        product = self.data_manager.get_product(created_product['id'])
        self.assertIsNone(product)
        
        # Non-existent product
        result = self.data_manager.delete_product(999)
        self.assertFalse(result)
    
    def test_create_customer(self):
        """Test creating a new customer"""
        customer = self.data_manager.create_customer("John Doe", "john@example.com", "123-456-7890")
        
        self.assertEqual(customer['name'], "John Doe")
        self.assertEqual(customer['email'], "john@example.com")
        self.assertEqual(customer['phone'], "123-456-7890")
        self.assertEqual(customer['id'], 1)
    
    def test_get_all_customers(self):
        """Test getting all customers"""
        # Initially empty
        customers = self.data_manager.get_all_customers()
        self.assertEqual(len(customers), 0)
        
        # Add customers
        self.data_manager.create_customer("John Doe", "john@example.com", "123-456-7890")
        self.data_manager.create_customer("Jane Smith", "jane@example.com", "098-765-4321")
        
        customers = self.data_manager.get_all_customers()
        self.assertEqual(len(customers), 2)
    
    def test_get_customer(self):
        """Test getting a specific customer"""
        # Create a customer
        created_customer = self.data_manager.create_customer("John Doe", "john@example.com", "123-456-7890")
     
      # Get the customer
        customer = self.data_manager.get_customer(created_customer['id'])
        self.assertIsNotNone(customer)
        self.assertEqual(customer['name'], "John Doe")
        
        # Non-existent customer
        customer = self.data_manager.get_customer(999)
        self.assertIsNone(customer)
    
