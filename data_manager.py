import json
import os
import logging
from typing import List, Dict, Optional

class DataManager:
    """Handles CRUD operations for products and customers using JSON files"""
    
    def __init__(self):
        self.products_file = 'products.json'
        self.customers_file = 'customers.json'
        self._ensure_files_exist()
    
    def _ensure_files_exist(self):
        """Create JSON files if they don't exist"""
        if not os.path.exists(self.products_file):
            with open(self.products_file, 'w') as f:
                json.dump([], f)
        
        if not os.path.exists(self.customers_file):
            with open(self.customers_file, 'w') as f:
                json.dump([], f)
    
    def _read_json_file(self, filename: str) -> List[Dict]:
        """Read data from JSON file"""
        try:
            with open(filename, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError) as e:
            logging.error(f"Error reading {filename}: {str(e)}")
            return []
    
    def _write_json_file(self, filename: str, data: List[Dict]):
        """Write data to JSON file"""
        try:
            with open(filename, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            logging.error(f"Error writing to {filename}: {str(e)}")
            raise
    
    def _get_next_id(self, data: List[Dict]) -> int:
        """Generate next available ID"""
        if not data:
            return 1
        return max(item['id'] for item in data) + 1
    
    # Product CRUD Operations
    def get_all_products(self) -> List[Dict]:
        """Get all products"""
        return self._read_json_file(self.products_file)
    
    def get_product(self, product_id: int) -> Optional[Dict]:
        """Get a specific product by ID"""
        products = self._read_json_file(self.products_file)
        return next((p for p in products if p['id'] == product_id), None)
    
    def create_product(self, name: str, price: float, stock: int) -> Dict:
        """Create a new product"""
        products = self._read_json_file(self.products_file)
        new_product = {
            'id': self._get_next_id(products),
            'name': name.strip(),
            'price': price,
            'stock': stock
        }
        products.append(new_product)
        self._write_json_file(self.products_file, products)
        return new_product
    
    def update_product(self, product_id: int, updates: Dict) -> Optional[Dict]:
        """Update an existing product"""
        products = self._read_json_file(self.products_file)
        
        for product in products:
            if product['id'] == product_id:
                # Update only provided fields
                if 'name' in updates:
                    product['name'] = updates['name'].strip()
                if 'price' in updates:
                    product['price'] = updates['price']
                if 'stock' in updates:
                    product['stock'] = updates['stock']
                
                self._write_json_file(self.products_file, products)
                return product
        
        return None
    
    def delete_product(self, product_id: int) -> bool:
        """Delete a product"""
        products = self._read_json_file(self.products_file)
        original_length = len(products)
        
        products = [p for p in products if p['id'] != product_id]
        
        if len(products) < original_length:
            self._write_json_file(self.products_file, products)
            return True
        
        return False
    
    # Customer CRUD Operations
    def get_all_customers(self) -> List[Dict]:
        """Get all customers"""
        return self._read_json_file(self.customers_file)
    
    def get_customer(self, customer_id: int) -> Optional[Dict]:
        """Get a specific customer by ID"""
        customers = self._read_json_file(self.customers_file)
        return next((c for c in customers if c['id'] == customer_id), None)
    
    def create_customer(self, name: str, email: str, phone: str) -> Dict:
        """Create a new customer"""
        customers = self._read_json_file(self.customers_file)
        new_customer = {
            'id': self._get_next_id(customers),
            'name': name.strip(),
            'email': email.strip(),
            'phone': phone.strip()
        }
        customers.append(new_customer)
        self._write_json_file(self.customers_file, customers)
        return new_customer
    
    def update_customer(self, customer_id: int, updates: Dict) -> Optional[Dict]:
        """Update an existing customer"""
        customers = self._read_json_file(self.customers_file)
        
        for customer in customers:
            if customer['id'] == customer_id:
                # Update only provided fields
                if 'name' in updates:
                    customer['name'] = updates['name'].strip()
                if 'email' in updates:
                    customer['email'] = updates['email'].strip()
                if 'phone' in updates:
                    customer['phone'] = updates['phone'].strip()
                
                self._write_json_file(self.customers_file, customers)
                return customer
        
        return None
    
    def delete_customer(self, customer_id: int) -> bool:
        """Delete a customer"""
        customers = self._read_json_file(self.customers_file)
        original_length = len(customers)
        
        customers = [c for c in customers if c['id'] != customer_id]
        
        if len(customers) < original_length:
            self._write_json_file(self.customers_file, customers)
            return True
        
        return False
