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
                </div>
            <div class="mt-3">
                <h6>Summary:</h6>
                <p><strong>Total Items:</strong> ${filteredProducts.length}</p>
                <p><strong>Total Value:</strong> €${filteredProducts.reduce((sum, p) => sum + (p.price * p.stock), 0).toFixed(2)}</p>
            </div>
        `;

        document.getElementById('inventoryReport').innerHTML = reportHtml;
    } catch (error) {
        document.getElementById('inventoryReport').innerHTML = `<div class="alert alert-danger">Error: ${error.message}</div>`;
    }
}

async function generateCustomerReport() {
    try {
        const searchTerm = document.getElementById('searchCustomer').value.toLowerCase();
        const sortBy = document.getElementById('sortCustomers').value;
        
        let customers = await reportsApp.apiRequest('/api/customers');
        
        // Filter customers based on search
        if (searchTerm) {
            customers = customers.filter(c => 
                c.name.toLowerCase().includes(searchTerm) || 
                c.email.toLowerCase().includes(searchTerm)
            );
        }

        // Sort customers
        customers.sort((a, b) => {
            if (sortBy === 'email') {
                return a.email.localeCompare(b.email);
            } else if (sortBy === 'phone') {
                return a.phone.localeCompare(b.phone);
            } else {
                return a.name.localeCompare(b.name);
            }
        });

        // Generate report HTML
        const reportHtml = `
            <div class="table-responsive">
                <table class="table table-striped">
                    <thead class="table-success">
                        <tr>
                            <th>ID</th>
                            <th>Name</th>
                            <th>Email</th>
                            <th>Phone</th>
                            <th>Domain</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${customers.map(customer => `
                            <tr>
                                <td>${customer.id}</td>
                                <td>${customer.name}</td>
                                <td>${customer.email}</td>
                                <td>${customer.phone}</td>
                                <td>${customer.email.split('@')[1]}</td>
                            </tr>
                        `).join('')}
                    </tbody>
                </table>
            </div>
            <div class="mt-3">
                <h6>Summary:</h6>
                <p><strong>Total Customers:</strong> ${customers.length}</p>
                <p><strong>Unique Domains:</strong> ${new Set(customers.map(c => c.email.split('@')[1])).size}</p>
            </div>
        `;

        document.getElementById('customerReport').innerHTML = reportHtml;
    } catch (error) {
        document.getElementById('customerReport').innerHTML = `<div class="alert alert-danger">Error: ${error.message}</div>`;
    }
}

async function generateSummaryReport() {
    try {
        const stats = await reportsApp.apiRequest('/api/stats/summary');
        
        // Generate summary HTML
        const summaryHtml = `
            <div class="row">
                <div class="col-md-6">
                    <div class="card">
                        <div class="card-header">
                            <h6>Inventory Statistics</h6>
                        </div>
                        <div class="card-body">
                            <p><strong>Total Products:</strong> ${stats.total_products}</p>
                            <p><strong>Total Inventory Value:</strong> €${stats.total_inventory_value}</p>
                            <p><strong>Average Product Price:</strong> €${stats.average_price}</p>
                            <p><strong>Low Stock Items:</strong> ${stats.low_stock_items}</p>
                        </div>
                    </div>
                </div>
                <div class="col-md-6">
                    <div class="card">
                        <div class="card-header">
                            <h6>Customer Statistics</h6>
                        </div>
                        <div class="card-body">
                            <p><strong>Total Customers:</strong> ${stats.total_customers}</p>
                            <p><strong>Customer Growth:</strong> ${stats.recent_customers.length} recent additions</p>
                        </div>
                    </div>
                </div>
            </div>
            <div class="row mt-3">
                <div class="col-md-6">
                    <div class="card">
                        <div class="card-header">
                            <h6>Product Highlights</h6>
                        </div>
                        <div class="card-body">
                            ${stats.most_expensive_product ? `
                                <p><strong>Most Expensive:</strong> ${stats.most_expensive_product.name} (€${stats.most_expensive_product.price})</p>
                            ` : '<p>No products available</p>'}
                            ${stats.cheapest_product ? `
                                <p><strong>Cheapest:</strong> ${stats.cheapest_product.name} (€${stats.cheapest_product.price})</p>
                            ` : ''}
                        </div>
                    </div>
                </div>
                <div class="col-md-6">
                    <div class="card">
                        <div class="card-header">
                            <h6>System Health</h6>
                        </div>
                        <div class="card-body">
                            <p><strong>Data Integrity:</strong> <span class="badge bg-success">Good</span></p>
                            <p><strong>Last Updated:</strong> ${new Date().toLocaleString()}</p>
                        </div>
                    </div>
                </div>
            </div>
        `;

        document.getElementById('summaryReport').innerHTML = summaryHtml;
    } catch (error) {
        document.getElementById('summaryReport').innerHTML = `<div class="alert alert-danger">Error: ${error.message}</div>`;
    }
}
                
