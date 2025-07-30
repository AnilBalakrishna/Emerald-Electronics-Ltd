import unittest
import json
import os
import tempfile
import shutil
from app import app

class TestAPI(unittest.TestCase):
    
    def setUp(self):
        """Set up test environment"""
        self.test_dir = tempfile.mkdtemp()
        self.original_dir = os.getcwd()
        os.chdir(self.test_dir)
        
        app.config['TESTING'] = True
        self.client = app.test_client()
    
    def tearDown(self):
        """Clean up test environment"""
        os.chdir(self.original_dir)
        shutil.rmtree(self.test_dir)
    
    def test_get_products_empty(self):
        """Test getting products when none exist"""
        response = self.client.get('/api/products')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertEqual(len(data), 0)
    
    def test_create_product(self):
        """Test creating a new product"""
        product_data = {
            'name': 'Test Product',
            'price': 99.99,
            'stock': 10
        }
        
        response = self.client.post('/api/products', 
                                  data=json.dumps(product_data),
                                  content_type='application/json')
        
        self.assertEqual(response.status_code, 201)
        
        data = json.loads(response.data)
        self.assertEqual(data['name'], 'Test Product')
        self.assertEqual(data['price'], 99.99)
        self.assertEqual(data['stock'], 10)
        self.assertEqual(data['id'], 1)
    
    def test_create_product_validation(self):
        """Test product creation validation"""
        # Missing required fields
        response = self.client.post('/api/products', 
                                  data=json.dumps({'name': 'Test'}),
                                  content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        
        # Invalid price
        product_data = {
            'name': 'Test Product',
            'price': -10,
            'stock': 10
        }
        
        response = self.client.post('/api/products', 
                                  data=json.dumps(product_data),
                                  content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
    
    def test_get_product(self):
        """Test getting a specific product"""
        # Create a product first
        product_data = {
            'name': 'Test Product',
            'price': 99.99,
            'stock': 10
        }
        
        response = self.client.post('/api/products', 
                                  data=json.dumps(product_data),
                                  content_type='application/json')
        
        created_product = json.loads(response.data)
        
        # Get the product
        response = self.client.get(f'/api/products/{created_product["id"]}')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertEqual(data['name'], 'Test Product')
        
        # Non-existent product
        response = self.client.get('/api/products/999')
        self.assertEqual(response.status_code, 404)
    
    def test_update_product(self):
        """Test updating a product"""
        # Create a product first
        product_data = {
            'name': 'Test Product',
            'price': 99.99,
            'stock': 10
        }

  response = self.client.post('/api/products', 
                                  data=json.dumps(product_data),
                                  content_type='application/json')
        
        created_product = json.loads(response.data)
        
        # Update the product
        update_data = {
            'name': 'Updated Product',
            'price': 149.99
        }
        
        response = self.client.put(f'/api/products/{created_product["id"]}', 
                                 data=json.dumps(update_data),
                                 content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertEqual(data['name'], 'Updated Product')
        self.assertEqual(data['price'], 149.99)
        self.assertEqual(data['stock'], 10)  # Unchanged
    
    def test_delete_product(self):
        """Test deleting a product"""
        # Create a product first
        product_data = {
            'name': 'Test Product',
            'price': 99.99,
            'stock': 10
        }
        
        response = self.client.post('/api/products', 
                                  data=json.dumps(product_data),
                                  content_type='application/json')
        
        created_product = json.loads(response.data)
        
        # Delete the product
        response = self.client.delete(f'/api/products/{created_product["id"]}')
        self.assertEqual(response.status_code, 200)
        
        # Verify deletion
        response = self.client.get(f'/api/products/{created_product["id"]}')
        self.assertEqual(response.status_code, 404)
    
    def test_create_customer(self):
        """Test creating a new customer"""
        customer_data = {
            'name': 'John Doe',
            'email': 'john@example.com',
            'phone': '123-456-7890'
        }
        
        response = self.client.post('/api/customers', 
                                  data=json.dumps(customer_data),
                                  content_type='application/json')
        
        self.assertEqual(response.status_code, 201)
        
        data = json.loads(response.data)
        self.assertEqual(data['name'], 'John Doe')
        self.assertEqual(data['email'], 'john@example.com')
        self.assertEqual(data['phone'], '123-456-7890')
        self.assertEqual(data['id'], 1)
    
    def test_create_customer_validation(self):
        """Test customer creation validation"""
        # Invalid email
        customer_data = {
            'name': 'John Doe',
            'email': 'invalid-email',
            'phone': '123-456-7890'
        }
        
        response = self.client.post('/api/customers', 
                                  data=json.dumps(customer_data),
                                  content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
    
    def test_integration_full_crud(self):
        """Integration test: Full CRUD operations for both products and customers"""
        # Create a product
        product_data = {
            'name': 'iPhone 15',
            'price': 999.99,
            'stock': 5
        }
        
        response = self.client.post('/api/products', 
                                  data=json.dumps(product_data),
                                  content_type='application/json')
        
        self.assertEqual(response.status_code, 201)
        product = json.loads(response.data)
        
        # Create a customer
        customer_data = {
            'name': 'Alice Johnson',
            'email': 'alice@example.com',
            'phone': '087-123-4567'
        }

response = self.client.post('/api/customers', 
                                  data=json.dumps(customer_data),
                                  content_type='application/json')
        
        self.assertEqual(response.status_code, 201)
        customer = json.loads(response.data)
        
        # Read both
        response = self.client.get('/api/products')
        products = json.loads(response.data)
        self.assertEqual(len(products), 1)
        
        response = self.client.get('/api/customers')
        customers = json.loads(response.data)
        self.assertEqual(len(customers), 1)
        
        # Update both
        response = self.client.put(f'/api/products/{product["id"]}', 
                                 data=json.dumps({'price': 899.99}),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 200)
        
        response = self.client.put(f'/api/customers/{customer["id"]}', 
                                 data=json.dumps({'phone': '087-999-8888'}),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 200)
        
        # Delete both
        response = self.client.delete(f'/api/products/{product["id"]}')
        self.assertEqual(response.status_code, 200)
        
        response = self.client.delete(f'/api/customers/{customer["id"]}')
        self.assertEqual(response.status_code, 200)
        
        # Verify deletion
        response = self.client.get('/api/products')
        products = json.loads(response.data)
        self.assertEqual(len(products), 0)
        
        response = self.client.get('/api/customers')
        customers = json.loads(response.data)
        self.assertEqual(len(customers), 0)

if __name__ == '__main__':
    unittest.main()
  
