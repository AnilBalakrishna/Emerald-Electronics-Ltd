import os
import logging
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from data_manager import DataManager

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Create Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "emerald-electronics-secret-key")

# Enable CORS for API access
CORS(app)

# Initialize data manager
data_manager = DataManager()

# Routes for serving the frontend
@app.route('/')
def dashboard():
    """Serve the dashboard page"""
    return render_template('dashboard.html')

@app.route('/manage')
def index():
    """Serve the data management page"""
    return render_template('index.html')

@app.route('/reports')
def reports():
    """Serve the reports page"""
    return render_template('reports.html')

# API Routes for Products
@app.route('/api/products', methods=['GET'])
def get_products():
    """Get all products"""
    try:
        products = data_manager.get_all_products()
        return jsonify(products)
    except Exception as e:
        logging.error(f"Error getting products: {str(e)}")
        return jsonify({'error': 'Failed to retrieve products'}), 500

@app.route('/api/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    """Get a specific product by ID"""
    try:
         product = data_manager.get_product(product_id)
        if product:
            return jsonify(product)
        return jsonify({'error': 'Product not found'}), 404
    except Exception as e:
        logging.error(f"Error getting product {product_id}: {str(e)}")
        return jsonify({'error': 'Failed to retrieve product'}), 500

@app.route('/api/products', methods=['POST'])
def create_product():
    """Create a new product"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['name', 'price', 'stock']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required fields: name, price, stock'}), 400
        
        # Validate data types
        try:
            data['price'] = float(data['price'])
            data['stock'] = int(data['stock'])
        except ValueError:
            return jsonify({'error': 'Invalid data types: price must be a number, stock must be an integer'}), 400
        
        # Validate values
        if data['price'] < 0:
            return jsonify({'error': 'Price cannot be negative'}), 400
        if data['stock'] < 0:
            return jsonify({'error': 'Stock cannot be negative'}), 400
        if not data['name'].strip():
            return jsonify({'error': 'Product name cannot be empty'}), 400
        
        product = data_manager.create_product(data['name'], data['price'], data['stock'])
        return jsonify(product), 201
    except Exception as e:
        logging.error(f"Error creating product: {str(e)}")
        return jsonify({'error': 'Failed to create product'}), 500

@app.route('/api/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    """Update an existing product"""
    try:
        data = request.get_json()
        
        # Validate data if provided
        if 'price' in data:
            try:
                data['price'] = float(data['price'])
                if data['price'] < 0:
                    return jsonify({'error': 'Price cannot be negative'}), 400
            except ValueError:
                return jsonify({'error': 'Invalid price format'}), 400
        
        if 'stock' in data:
            try:
                data['stock'] = int(data['stock'])
                if data['stock'] < 0:
                    return jsonify({'error': 'Stock cannot be negative'}), 400
            except ValueError:
                return jsonify({'error': 'Invalid stock format'}), 400
        
        if 'name' in data and not data['name'].strip():
            return jsonify({'error': 'Product name cannot be empty'}), 400
        
        product = data_manager.update_product(product_id, data)
        if product:
            return jsonify(product)
        return jsonify({'error': 'Product not found'}), 404
    except Exception as e:
        logging.error(f"Error updating product {product_id}: {str(e)}")
        return jsonify({'error': 'Failed to update product'}), 500

@app.route('/api/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    """Delete a product"""
    try:
        if data_manager.delete_product(product_id):
            return jsonify({'message': 'Product deleted successfully'})
        return jsonify({'error': 'Product not found'}), 404
    except Exception as e:
        logging.error(f"Error deleting product {product_id}: {str(e)}")
        return jsonify({'error': 'Failed to delete product'}), 500

# API Routes for Customers
@app.route('/api/customers', methods=['GET'])
def get_customers():
    """Get all customers"""
    try:
        customers = data_manager.get_all_customers()
        return jsonify(customers)
    except Exception as e:
        logging.error(f"Error getting customers: {str(e)}")
        return jsonify({'error': 'Failed to retrieve customers'}), 500

@app.route('/api/customers/<int:customer_id>', methods=['GET'])
def get_customer(customer_id):
    """Get a specific customer by ID"""
    try:
        customer = data_manager.get_customer(customer_id)
        if customer:
            return jsonify(customer)
        return jsonify({'error': 'Customer not found'}), 404
    except Exception as e:
        logging.error(f"Error getting customer {customer_id}: {str(e)}")
        return jsonify({'error': 'Failed to retrieve customer'}), 500

@app.route('/api/customers', methods=['POST'])
def create_customer():
    """Create a new customer"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['name', 'email', 'phone']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required fields: name, email, phone'}), 400
        
        # Validate values
        if not data['name'].strip():
            return jsonify({'error': 'Customer name cannot be empty'}), 400
        if not data['email'].strip() or '@' not in data['email']:
            return jsonify({'error': 'Invalid email format'}), 400
        if not data['phone'].strip():
            return jsonify({'error': 'Phone number cannot be empty'}), 400
        
        customer = data_manager.create_customer(data['name'], data['email'], data['phone'])
        return jsonify(customer), 201
    except Exception as e:
        logging.error(f"Error creating customer: {str(e)}")
        return jsonify({'error': 'Failed to create customer'}), 500

@app.route('/api/customers/<int:customer_id>', methods=['PUT'])
def update_customer(customer_id):
    """Update an existing customer"""
    try:
        data = request.get_json()
        
        # Validate data if provided
        if 'name' in data and not data['name'].strip():
            return jsonify({'error': 'Customer name cannot be empty'}), 400
        if 'email' in data and (not data['email'].strip() or '@' not in data['email']):
            return jsonify({'error': 'Invalid email format'}), 400
        if 'phone' in data and not data['phone'].strip():
            return jsonify({'error': 'Phone number cannot be empty'}), 400
        
        customer = data_manager.update_customer(customer_id, data)
        if customer:
            return jsonify(customer)
        return jsonify({'error': 'Customer not found'}), 404
    except Exception as e:
        logging.error(f"Error updating customer {customer_id}: {str(e)}")
        return jsonify({'error': 'Failed to update customer'}), 500

app.route('/api/customers/<int:customer_id>', methods=['DELETE'])
def d@elete_customer(customer_id):
    """Delete a customer"""
    try:
        if data_manager.delete_customer(customer_id):
            return jsonify({'message': 'Customer deleted successfully'})
        return jsonify({'error': 'Customer not found'}), 404
    except Exception as e:
        logging.error(f"Error deleting customer {customer_id}: {str(e)}")
        return jsonify({'error': 'Failed to delete customer'}), 500
                        
# API Routes for Statistics and Reports
@app.route('/api/stats/summary', methods=['GET'])
def get_summary_stats():
    """Get summary statistics"""
    try:
        products = data_manager.get_all_products()
        customers = data_manager.get_all_customers()
        
        # Calculate statistics
        total_products = len(products)
        total_customers = len(customers)
        low_stock_items = len([p for p in products if p['stock'] <= 5])
        total_inventory_value = sum(p['price'] * p['stock'] for p in products)
        
        # Find most expensive and cheapest products
        most_expensive = max(products, key=lambda x: x['price']) if products else None
        cheapest = min(products, key=lambda x: x['price']) if products else None
        
        stats = {
            'total_products': total_products,
            'total_customers': total_customers,
            'low_stock_items': low_stock_items,
            'total_inventory_value': round(total_inventory_value, 2),
            'most_expensive_product': most_expensive,
            'cheapest_product': cheapest,
            'average_price': round(sum(p['price'] for p in products) / len(products), 2) if products else 0,
            'recent_products': products[-5:] if len(products) >= 5 else products,
            'recent_customers': customers[-5:] if len(customers) >= 5 else customers
        }
        
        return jsonify(stats)
    except Exception as e:
        logging.error(f"Error getting summary stats: {str(e)}")
        return jsonify({'error': 'Failed to retrieve statistics'}), 500

@app.route('/api/products/search', methods=['GET'])
def search_products():
    """Search products by name"""
    try:
        query = request.args.get('q', '').lower()
        sort_by = request.args.get('sort', 'name')
        
        products = data_manager.get_all_products()
        
        # Filter by search query
        if query:
            products = [p for p in products if query in p['name'].lower()]
        
        # Sort products
        if sort_by == 'price':
            products.sort(key=lambda x: x['price'])
        elif sort_by == 'stock':
            products.sort(key=lambda x: x['stock'])
        else:  # name
            products.sort(key=lambda x: x['name'].lower())
        
        return jsonify(products)
    except Exception as e:
        logging.error(f"Error searching products: {str(e)}")
        return jsonify({'error': 'Failed to search products'}), 500

@app.route('/api/customers/search', methods=['GET'])
def search_customers():
    """Search customers by name or email"""
    try:
        query = request.args.get('q', '').lower()
        sort_by = request.args.get('sort', 'name')
        
        customers = data_manager.get_all_customers()
        
        # Filter by search query
        if query:
            customers = [c for c in customers if query in c['name'].lower() or query in c['email'].lower()]
        
        # Sort customers
        if sort_by == 'email':
            customers.sort(key=lambda x: x['email'].lower())
        elif sort_by == 'phone':
            customers.sort(key=lambda x: x['phone'])
        else:  # name
            customers.sort(key=lambda x: x['name'].lower())
        
        return jsonify(customers)
    except Exception as e:
        logging.error(f"Error searching customers: {str(e)}")
        return jsonify({'error': 'Failed to search customers'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
