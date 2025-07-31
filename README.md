# Emerald Electronics Ltd - Information System

A basic Information System for Emerald Electronics Ltd, a small Dublin electronics shop. This system provides CRUD (Create, Read, Update, Delete) operations for managing products and customers using Flask API backend and JavaScript frontend.

## Features

- **Product Management**: Add, view, edit, and delete electronic products
- **Customer Management**: Add, view, edit, and delete customer information
- **API-based Architecture**: RESTful API with JSON responses
- **Data Persistence**: Uses JSON files for data storage
- **Responsive UI**: Bootstrap-based interface with dark theme
- **Form Validation**: Client-side and server-side validation
- **Error Handling**: Comprehensive error handling and user feedback

## Technology Stack

- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Data Storage**: JSON files (products.json, customers.json)
- **Styling**: Bootstrap 5 with dark theme
- **Testing**: Python unittest framework

## System Requirements

- Python 3.7+
- Flask
- Flask-CORS

## Installation and Setup

1. **Clone the repository** (or download the files)
2. **Install dependencies**:
   ```bash
   pip install flask flask-cors
   ```
3. **Run the application**:
   ```bash
   python main.py
   ```
4. **Access the application**:
   Open your browser and go to `http://localhost:5000`

## Running Tests
To run the tests, execute the following command in your terminal:
```bash
python -m unittest discover -s tests
