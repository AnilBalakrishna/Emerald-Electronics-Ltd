class EmeraldElectronicsApp {
    constructor() {
        this.apiBase = '';
        this.currentEditingProduct = null;
        this.currentEditingCustomer = null;
        this.productModal = null;
        this.customerModal = null;
        this.allProducts = [];
        this.allCustomers = [];
        this.filteredProducts = [];
        this.filteredCustomers = [];
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.setupModals();
        this.loadProducts();
        this.loadCustomers();
    }

    setupModals() {
        this.productModal = new bootstrap.Modal(document.getElementById('productModal'));
        this.customerModal = new bootstrap.Modal(document.getElementById('customerModal'));
    }

    setupEventListeners() {
        // Product form submission
        document.getElementById('productForm').addEventListener('submit', (e) => {
            e.preventDefault();
            this.handleProductSubmit();
        });

        // Customer form submission
        document.getElementById('customerForm').addEventListener('submit', (e) => {
            e.preventDefault();
            this.handleCustomerSubmit();
        });

        // Modal event listeners
        document.getElementById('productModal').addEventListener('hidden.bs.modal', () => {
            this.resetProductForm();
        });

        document.getElementById('customerModal').addEventListener('hidden.bs.modal', () => {
            this.resetCustomerForm();
        });

        // Tab switching
        document.addEventListener('shown.bs.tab', (e) => {
            if (e.target.getAttribute('data-bs-target') === '#products') {
                this.loadProducts();
            } else if (e.target.getAttribute('data-bs-target') === '#customers') {
                this.loadCustomers();
            }
        });
    }

    // Utility methods
    showAlert(containerId, message, type = 'danger') {
        const alertDiv = document.getElementById(containerId);
        alertDiv.className = `alert alert-${type}`;
        alertDiv.textContent = message;
        alertDiv.style.display = 'block';
        
        setTimeout(() => {
            alertDiv.style.display = 'none';
        }, 5000);
    }

    showLoading(loadingId, show = true) {
        document.getElementById(loadingId).style.display = show ? 'block' : 'none';
    }

    resetProductForm() {
        document.getElementById('productForm').reset();
        document.getElementById('productId').value = '';
        document.getElementById('productModalLabel').textContent = 'Add Product';
        document.getElementById('productSubmitBtn').textContent = 'Add Product';
        this.currentEditingProduct = null;
    }

    resetCustomerForm() {
        document.getElementById('customerForm').reset();
        document.getElementById('customerId').value = '';
        document.getElementById('customerModalLabel').textContent = 'Add Customer';
        document.getElementById('customerSubmitBtn').textContent = 'Add Customer';
        this.currentEditingCustomer = null;
    }

    // API methods
    async apiRequest(endpoint, options = {}) {
        try {
            const response = await fetch(`${this.apiBase}${endpoint}`, {
                headers: {
                    'Content-Type': 'application/json',
                    ...options.headers
                },
                ...options
            });
          
if (!response.ok) {
                const error = await response.json();
                throw new Error(error.error || 'Request failed');
            }

            return await response.json();
        } catch (error) {
            console.error('API request failed:', error);
            throw error;
        }
    }

    // Product methods
    async loadProducts() {
        this.showLoading('productsLoading');
        try {
            const products = await this.apiRequest('/api/products');
            this.allProducts = products;
            this.filteredProducts = products;
            this.renderProducts(products);
        } catch (error) {
            this.showAlert('productsAlert', `Failed to load products: ${error.message}`);
        } finally {
            this.showLoading('productsLoading', false);
        }
    }

    searchProducts() {
        const query = document.getElementById('productSearch').value.toLowerCase();
        this.filteredProducts = this.allProducts.filter(product => 
            product.name.toLowerCase().includes(query)
        );
        this.sortProducts();
    }

    sortProducts() {
        const sortBy = document.getElementById('productSort').value;
        this.filteredProducts.sort((a, b) => {
            if (sortBy === 'price') {
                return a.price - b.price;
            } else if (sortBy === 'stock') {
                return a.stock - b.stock;
            } else {
                return a.name.localeCompare(b.name);
            }
        });
        this.renderProducts(this.filteredProducts);
    }

    renderProducts(products) {
        const tbody = document.getElementById('productsTableBody');
        
        if (products.length === 0) {
            tbody.innerHTML = '<tr><td colspan="5" class="text-center text-muted">No products found. Add your first product to get started.</td></tr>';
            return;
        }

        tbody.innerHTML = products.map(product => `
            <tr>
                <td>${product.id}</td>
                <td>${product.name}</td>
                <td>€${product.price.toFixed(2)}</td>
                <td>${product.stock}</td>
                <td>
                    <button class="btn btn-sm btn-outline-primary me-1" onclick="app.editProduct(${product.id})">Edit</button>
                    <button class="btn btn-sm btn-outline-danger" onclick="app.deleteProduct(${product.id})">Delete</button>
                </td>
            </tr>
        `).join('');
    }

    async handleProductSubmit() {
        const form = document.getElementById('productForm');
        const formData = new FormData(form);
        
        const productData = {
            name: formData.get('name'),
            price: parseFloat(formData.get('price')),
            stock: parseInt(formData.get('stock'))
        };

        try {
            if (this.currentEditingProduct) {
                // Update existing product
                await this.apiRequest(`/api/products/${this.currentEditingProduct}`, {
                    method: 'PUT',
                    body: JSON.stringify(productData)
                });
                this.showAlert('productsAlert', 'Product updated successfully!', 'success');
            } else {
                // Create new product
                await this.apiRequest('/api/products', {
                    method: 'POST',
                    body: JSON.stringify(productData)
                });
                this.showAlert('productsAlert', 'Product added successfully!', 'success');
            }

            this.productModal.hide();
            this.loadProducts();
        } catch (error) {
            this.showAlert('productsAlert', `Failed to save product: ${error.message}`);
        }
    }

    async editProduct(productId) {
        try {
            const product = await this.apiRequest(`/api/products/${productId}`);
            
            // Fill form with product data
            document.getElementById('productId').value = product.id;
            document.getElementById('productName').value = product.name;
            document.getElementById('productPrice').value = product.price;
            document.getElementById('productStock').value = product.stock;
            
            // Update modal for editing mode
            this.currentEditingProduct = productId;
            document.getElementById('productModalLabel').textContent = 'Edit Product';
            document.getElementById('productSubmitBtn').textContent = 'Update Product';
            
            // Show modal
            this.productModal.show();
        } catch (error) {
            this.showAlert('productsAlert', `Failed to load product: ${error.message}`);
        }
    }

    async deleteProduct(productId) {
        if (!confirm('Are you sure you want to delete this product?')) {
            return;
        }

        try {
            await this.apiRequest(`/api/products/${productId}`, {
                method: 'DELETE'
            });
            this.showAlert('productsAlert', 'Product deleted successfully!', 'success');
            this.loadProducts();
        } catch (error) {
            this.showAlert('productsAlert', `Failed to delete product: ${error.message}`);
        }
    }

    // Customer methods
    async loadCustomers() {
        this.showLoading('customersLoading');
        try {
            const customers = await this.apiRequest('/api/customers');
            this.allCustomers = customers;
            this.filteredCustomers = customers;
            this.renderCustomers(customers);
        } catch (error) {
            this.showAlert('customersAlert', `Failed to load customers: ${error.message}`);
        } finally {
            this.showLoading('customersLoading', false);
        }
    }

