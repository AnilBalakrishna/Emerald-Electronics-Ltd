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
