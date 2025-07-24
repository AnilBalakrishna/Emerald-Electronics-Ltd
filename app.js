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
          
