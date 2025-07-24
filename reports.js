class ReportsApp {
    constructor() {
        this.apiBase = '';
        this.init();
    }

    init() {
        // Initialize any setup if needed
        console.log('Reports app initialized');
    }

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
}

// Initialize the reports app
document.addEventListener('DOMContentLoaded', () => {
    window.reportsApp = new ReportsApp();
});

// Report generation functions
async function generateInventoryReport() {
    try {
        const sortBy = document.getElementById('sortBy').value;
        const filterStock = document.getElementById('filterStock').value;
        
        const products = await reportsApp.apiRequest('/api/products');
        
        // Filter products based on stock level
        let filteredProducts = products;
        if (filterStock === 'low') {
            filteredProducts = products.filter(p => p.stock <= 5);
        } else if (filterStock === 'medium') {
            filteredProducts = products.filter(p => p.stock > 5 && p.stock <= 20);
        } else if (filterStock === 'high') {
            filteredProducts = products.filter(p => p.stock > 20);
        }

        // Sort products
        filteredProducts.sort((a, b) => {
            if (sortBy === 'price') {
                return a.price - b.price;
            } else if (sortBy === 'stock') {
                return a.stock - b.stock;
            } else {
                return a.name.localeCompare(b.name);
            }
        });

        // Generate report HTML
        const reportHtml = `
            <div class="table-responsive">
                <table class="table table-striped">
                    <thead class="table-primary">
                        <tr>
                            <th>Product Name</th>
                            <th>Price</th>
                            <th>Stock</th>
                            <th>Value</th>
                            <th>Status</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${filteredProducts.map(product => `
                            <tr>
                                <td>${product.name}</td>
                                <td>€${product.price.toFixed(2)}</td>
                                <td>${product.stock}</td>
                                <td>€${(product.price * product.stock).toFixed(2)}</td>
                                <td>
                                    ${product.stock <= 5 ? 
                                        '<span class="badge bg-danger">Low Stock</span>' : 
                                        product.stock <= 20 ? 
                                        '<span class="badge bg-warning">Medium Stock</span>' : 
                                        '<span class="badge bg-success">Good Stock</span>'
                                    }
                                </td>
                            </tr>
                        `).join('')}
                    </tbody>
                </table>
                
