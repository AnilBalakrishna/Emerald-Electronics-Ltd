class DashboardApp {
    constructor() {
        this.apiBase = '';
        this.init();
    }

    init() {
        this.loadDashboardData();
    }

    async loadDashboardData() {
        try {
            const stats = await this.apiRequest('/api/stats/summary');
            this.renderDashboard(stats);
        } catch (error) {
            console.error('Failed to load dashboard data:', error);
            this.renderError();
        }
    }

    renderDashboard(stats) {
        // Update summary cards
        document.getElementById('totalProducts').textContent = stats.total_products;
        document.getElementById('totalCustomers').textContent = stats.total_customers;
        document.getElementById('lowStockItems').textContent = stats.low_stock_items;

        // Render recent products
        const recentProductsHtml = stats.recent_products.map(product => `
            <div class="mb-2">
                <strong>${product.name}</strong><br>
                <small class="text-muted">€${product.price.toFixed(2)} | Stock: ${product.stock}</small>
            </div>
        `).join('');
        document.getElementById('recentProducts').innerHTML = recentProductsHtml || '<p class="text-muted">No products available</p>';

        // Render recent customers
        const recentCustomersHtml = stats.recent_customers.map(customer => `
            <div class="mb-2">
                <strong>${customer.name}</strong><br>
                <small class="text-muted">${customer.email}</small>
            </div>
        `).join('');
        document.getElementById('recentCustomers').innerHTML = recentCustomersHtml || '<p class="text-muted">No customers available</p>';
    }

    renderError() {
        document.getElementById('totalProducts').textContent = 'Error';
        document.getElementById('totalCustomers').textContent = 'Error';
        document.getElementById('lowStockItems').textContent = 'Error';
        document.getElementById('recentProducts').innerHTML = '<p class="text-danger">Failed to load data</p>';
        document.getElementById('recentCustomers').innerHTML = '<p class="text-danger">Failed to load data</p>';
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

// Initialize the dashboard app
document.addEventListener('DOMContentLoaded', () => {
    window.dashboardApp = new DashboardApp();
});
