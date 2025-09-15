from flask import Flask, render_template_string, request, redirect, url_for, session, flash
import json
from functools import wraps

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Change this in production

# Sample products data with working image URLs
products = [
    {
        "id": 1,
        "name": "ScamKit 3000",
        "price": 299.99,
        "image": "https://images.unsplash.com/photo-1581092921461-eab62e97a780?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=600&q=80",
        "description": "Advanced multi-tool kit for all your technical needs. Features precision engineering and durable materials."
    },
    {
        "id": 2,
        "name": "Virtual Gadget Pro",
        "price": 159.99,
        "image": "https://images.unsplash.com/photo-1581092580497-e0d23cbdf1dc?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=600&q=80",
        "description": "Cutting-edge virtual gadget with immersive experience and intuitive controls."
    },
    {
        "id": 3,
        "name": "Fake Sword Deluxe",
        "price": 89.99,
        "image": "https://images.unsplash.com/photo-1579972668140-f7da53eee1dc?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=600&q=80",
        "description": "Decorative sword with authentic design. Perfect for display or cosplay purposes."
    },
    {
        "id": 4,
        "name": "Phantom Drone",
        "price": 449.99,
        "image": "https://images.unsplash.com/photo-1579829366248-204fe8413f31?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=600&q=80",
        "description": "High-performance drone with advanced flight capabilities and HD camera."
    },
    {
        "id": 5,
        "name": "Illusion VR Headset",
        "price": 349.99,
        "image": "https://images.unsplash.com/photo-1593118247619-e2d6f056869e?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=600&q=80",
        "description": "Immersive virtual reality headset with high-resolution displays and comfortable design."
    },
    {
        "id": 6,
        "name": "Ghost Camera",
        "price": 599.99,
        "image": "https://images.unsplash.com/photo-1516035069371-29a1b244cc32?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=600&q=80",
        "description": "Professional-grade camera with advanced features for stunning photography."
    },
    {
        "id": 7,
        "name": "Fake Gun Deluxe",
        "price": 129.99,
        "image": "https://images.unsplash.com/photo-1598284636625-62e8a8c63cf3?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=600&q=80",
        "description": "Replica firearm with realistic design and detailed craftsmanship."
    },
    {
        "id": 8,
        "name": "Cyber Watch",
        "price": 199.99,
        "image": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=600&q=80",
        "description": "Smartwatch with advanced health tracking and notification features."
    },
    {
        "id": 9,
        "name": "Virtual Sword Kit",
        "price": 79.99,
        "image": "https://images.unsplash.com/photo-1618331835716-6e46a5a3b4b6?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=600&q=80",
        "description": "Complete set of virtual reality swords for immersive gaming experiences."
    },
    {
        "id": 10,
        "name": "ScamBot 9000",
        "price": 899.99,
        "image": "https://images.unsplash.com/photo-1485827404703-89b55fcc595e?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=600&q=80",
        "description": "Advanced robotic assistant with AI capabilities and versatile functionality."
    }
]

# Fake members data
members = [
    {"id": 1, "name": "John Doe", "email": "john@example.com", "status": "Active"},
    {"id": 2, "name": "Jane Smith", "email": "jane@example.com", "status": "Active"},
    {"id": 3, "name": "Bob Johnson", "email": "bob@example.com", "status": "Inactive"}
]

# Admin credentials
ADMIN_EMAIL = "administrator@test.here"
ADMIN_PASSWORD = "1234567890@#৳%&*-+()"

# Admin decorator
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('admin_logged_in'):
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function

# HTML Templates with all content in one string for each page
def base_template(content, title="Rifat TestLabs"):
    return f'''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        body {{
            background-color: #f8f9fa;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }}
        .navbar {{
            background-color: #2c3e50;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .navbar-brand, .nav-link {{
            color: #ecf0f1 !important;
        }}
        .navbar-brand {{
            font-weight: bold;
            font-size: 1.5rem;
        }}
        .card {{
            border: none;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            transition: transform 0.3s;
        }}
        .card:hover {{
            transform: translateY(-5px);
        }}
        .product-img {{
            height: 200px;
            object-fit: cover;
            border-top-left-radius: 10px;
            border-top-right-radius: 10px;
        }}
        .hero-section {{
            background: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)), url('https://images.unsplash.com/photo-1467232004584-a241de8bcf5d?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1200&q=80');
            background-size: cover;
            background-position: center;
            color: white;
            padding: 100px 0;
            text-align: center;
            margin-bottom: 40px;
        }}
        .btn-primary {{
            background-color: #3498db;
            border: none;
            border-radius: 5px;
            padding: 10px 20px;
        }}
        .btn-primary:hover {{
            background-color: #2980b9;
        }}
        .admin-panel {{
            background-color: #f8f9fa;
            border-radius: 10px;
            padding: 20px;
            margin-top: 20px;
        }}
        footer {{
            background-color: #2c3e50;
            color: #ecf0f1;
            padding: 30px 0;
            margin-top: 50px;
        }}
        .img-placeholder {{
            height: 200px;
            background: linear-gradient(45deg, #6c757d, #adb5bd);
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: bold;
            border-top-left-radius: 10px;
            border-top-right-radius: 10px;
        }}
    </style>
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark">
        <div class="container">
            <a class="navbar-brand" href="/">Rifat TestLabs</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav ms-auto">
                    <li class="nav-item">
                        <a class="nav-link" href="/">Home</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="#products">Products</a>
                    </li>
                    {'<li class="nav-item"><a class="nav-link" href="/admin_panel">Admin Panel</a></li><li class="nav-item"><a class="nav-link" href="/admin_logout">Logout</a></li>' 
                     if session.get('admin_logged_in') else ''}
                </ul>
            </div>
        </div>
    </nav>

    {content}

    <footer class="text-center">
        <div class="container">
            <p>&copy; 2023 Rifat TestLabs. All products are fictional. No real transactions occur on this site.</p>
            <p>This is a demonstration website only.</p>
        </div>
    </footer>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
'''

# Routes
@app.route('/')
def home():
    product_cards = []
    for p in products:
        product_cards.append(f'''
            <div class="col-md-4 mb-4">
                <div class="card h-100">
                    <img src="{p['image']}" class="card-img-top product-img" alt="{p['name']}" 
                         onerror="this.onerror=null; this.parentNode.innerHTML='<div class=\\'img-placeholder\\'>{p["name"]}</div>';">
                    <div class="card-body">
                        <h5 class="card-title">{p['name']}</h5>
                        <p class="card-text">${p['price']:.2f}</p>
                        <p class="card-text text-muted">{p['description'][:80]}...</p>
                        <a href="/product/{p['id']}" class="btn btn-primary">View Details</a>
                    </div>
                </div>
            </div>
        ''')
    
    content = f'''
    <div class="hero-section">
        <div class="container">
            <h1 class="display-4">Welcome to Rifat TestLabs</h1>
            <p class="lead">Discover the latest in innovative technology and gadgets</p>
            <a href="#products" class="btn btn-primary btn-lg">Explore Products</a>
        </div>
    </div>

    <div class="container" id="products">
        <h2 class="text-center mb-5">Our Products</h2>
        <div class="row">
            {''.join(product_cards)}
        </div>
    </div>
    '''
    return render_template_string(base_template(content, "Rifat TestLabs - Home"))

@app.route('/product/<int:product_id>')
def product_details(product_id):
    product = next((p for p in products if p['id'] == product_id), None)
    if not product:
        return "Product not found", 404
        
    content = f'''
    <div class="container mt-5">
        <div class="row">
            <div class="col-md-6">
                <img src="{product['image']}" class="img-fluid rounded" alt="{product['name']}" 
                     onerror="this.onerror=null; this.src='https://via.placeholder.com/500x300/6c757d/ffffff?text=Image+Not+Available';">
            </div>
            <div class="col-md-6">
                <h1>{product['name']}</h1>
                <p class="text-muted">Product ID: #{product['id']}</p>
                <h3 class="text-primary">${product['price']:.2f}</h3>
                <p>{product['description']}</p>
                <div class="d-grid gap-2">
                    <a href="/checkout/{product['id']}" class="btn btn-primary btn-lg">Buy Now</a>
                    <a href="/" class="btn btn-outline-secondary">Continue Shopping</a>
                </div>
            </div>
        </div>
    </div>
    '''
    return render_template_string(base_template(content, f"Rifat TestLabs - {product['name']}"))

@app.route('/checkout/<int:product_id>', methods=['GET', 'POST'])
def checkout(product_id):
    product = next((p for p in products if p['id'] == product_id), None)
    if not product:
        return "Product not found", 404
    
    if request.method == 'POST':
        # In a real application, you would process the order here
        # For this demo, we'll just show a confirmation page
        import random
        order_id = random.randint(100000, 999999)
        
        content = f'''
        <div class="container mt-5">
            <div class="row justify-content-center">
                <div class="col-md-8">
                    <div class="card">
                        <div class="card-header bg-success text-white text-center">
                            <h3 class="mb-0"><i class="fas fa-check-circle"></i> Order Confirmed</h3>
                        </div>
                        <div class="card-body text-center">
                            <h4>Thank you for your order!</h4>
                            <p class="lead">Your order has been successfully placed.</p>
                            <div class="my-4">
                                <h5>Order Details</h5>
                                <p><strong>Product:</strong> {product['name']}</p>
                                <p><strong>Total:</strong> ${product['price'] + 10:.2f}</p>
                                <p><strong>Order #:</strong> {order_id}</p>
                            </div>
                            <p>A confirmation email has been sent to your email address.</p>
                            <a href="/" class="btn btn-primary">Continue Shopping</a>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        '''
        return render_template_string(base_template(content, "Rifat TestLabs - Order Confirmation"))
    
    content = f'''
    <div class="container mt-5">
        <div class="row justify-content-center">
            <div class="col-md-8">
                <div class="card">
                    <div class="card-header bg-primary text-white">
                        <h3 class="mb-0">Checkout</h3>
                    </div>
                    <div class="card-body">
                        <div class="row mb-4">
                            <div class="col-md-6">
                                <h5>Product Details</h5>
                                <img src="{product['image']}" class="img-fluid rounded mb-2" alt="{product['name']}" style="max-height: 200px;"
                                     onerror="this.onerror=null; this.src='https://via.placeholder.com/300x200/6c757d/ffffff?text=Product+Image';">
                                <h6>{product['name']}</h6>
                                <p class="text-primary">${product['price']:.2f}</p>
                            </div>
                            <div class="col-md-6">
                                <h5>Order Summary</h5>
                                <table class="table">
                                    <tr>
                                        <td>Subtotal:</td>
                                        <td>${product['price']:.2f}</td>
                                    </tr>
                                    <tr>
                                        <td>Shipping:</td>
                                        <td>$10.00</td>
                                    </tr>
                                    <tr>
                                        <td><strong>Total:</strong></td>
                                        <td><strong>${product['price'] + 10:.2f}</strong></td>
                                    </tr>
                                </table>
                            </div>
                        </div>
                        
                        <h5 class="mb-3">Shipping Information</h5>
                        <form method="POST">
                            <div class="row">
                                <div class="col-md-6 mb-3">
                                    <label for="firstName" class="form-label">First Name</label>
                                    <input type="text" class="form-control" id="firstName" name="firstName" required>
                                </div>
                                <div class="col-md-6 mb-3">
                                    <label for="lastName" class="form-label">Last Name</label>
                                    <input type="text" class="form-control" id="lastName" name="lastName" required>
                                </div>
                            </div>
                            <div class="mb-3">
                                <label for="email" class="form-label">Email</label>
                                <input type="email" class="form-control" id="email" name="email" required>
                            </div>
                            <div class="mb-3">
                                <label for="address" class="form-label">Address</label>
                                <input type="text" class="form-control" id="address" name="address" required>
                            </div>
                            <div class="row">
                                <div class="col-md-4 mb-3">
                                    <label for="city" class="form-label">City</label>
                                    <input type="text" class="form-control" id="city" name="city" required>
                                </div>
                                <div class="col-md-4 mb-3">
                                    <label for="state" class="form-label">State</label>
                                    <input type="text" class="form-control" id="state" name="state" required>
                                </div>
                                <div class="col-md-4 mb-3">
                                    <label for="zip" class="form-label">Zip</label>
                                    <input type="text" class="form-control" id="zip" name="zip" required>
                                </div>
                            </div>
                            <div class="d-grid">
                                <button type="submit" class="btn btn-primary btn-lg">Place Order</button>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    </div>
    '''
    return render_template_string(base_template(content, "Rifat TestLabs - Checkout"))

@app.route('/administration_panel', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        if email == ADMIN_EMAIL and password == ADMIN_PASSWORD:
            session['admin_logged_in'] = True
            return redirect('/admin_panel')
        else:
            flash('Invalid credentials. Please try again.', 'danger')
    
    content = '''
    <div class="container mt-5">
        <div class="row justify-content-center">
            <div class="col-md-6">
                <div class="card">
                    <div class="card-header bg-dark text-white">
                        <h3 class="mb-0">Admin Login</h3>
                    </div>
                    <div class="card-body">
                        <form method="POST">
                            <div class="mb-3">
                                <label for="email" class="form-label">Email</label>
                                <input type="email" class="form-control" id="email" name="email" required>
                            </div>
                            <div class="mb-3">
                                <label for="password" class="form-label">Password</label>
                                <input type="password" class="form-control" id="password" name="password" required>
                            </div>
                            <div class="d-grid">
                                <button type="submit" class="btn btn-primary">Login</button>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    </div>
    '''
    return render_template_string(base_template(content, "Rifat TestLabs - Admin Login"))

@app.route('/admin_panel')
@admin_required
def admin_panel():
    product_modals = []
    for p in products:
        product_modals.append(f'''
        <div class="modal fade" id="editProductModal{p['id']}" tabindex="-1">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">Edit Product</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                    </div>
                    <form method="POST" action="/edit_product/{p['id']}">
                        <div class="modal-body">
                            <div class="mb-3">
                                <label for="name{p['id']}" class="form-label">Name</label>
                                <input type="text" class="form-control" id="name{p['id']}" name="name" value="{p['name']}" required>
                            </div>
                            <div class="mb-3">
                                <label for="price{p['id']}" class="form-label">Price</label>
                                <input type="number" step="0.01" class="form-control" id="price{p['id']}" name="price" value="{p['price']}" required>
                            </div>
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
                            <button type="submit" class="btn btn-primary">Save Changes</button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
        ''')
    
    product_rows = []
    for p in products:
        product_rows.append(f'''
        <tr>
            <td>{p['id']}</td>
            <td>{p['name']}</td>
            <td>${p['price']:.2f}</td>
            <td>
                <button class="btn btn-sm btn-outline-primary" data-bs-toggle="modal" data-bs-target="#editProductModal{p['id']}">
                    Edit
                </button>
            </td>
        </tr>
        ''')
    
    member_rows = []
    for m in members:
        member_rows.append(f'''
        <tr>
            <td>{m['id']}</td>
            <td>{m['name']}</td>
            <td>{m['email']}</td>
            <td>
                <span class="badge {'bg-success' if m['status'] == 'Active' else 'bg-warning'}">
                    {m['status']}
                </span>
            </td>
        </tr>
        ''')
    
    content = f'''
    <div class="container mt-4">
        <h1 class="text-center mb-4">Admin Panel</h1>
        
        <div class="admin-panel">
            <h3>Product Management</h3>
            <div class="table-responsive">
                <table class="table table-striped">
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Name</th>
                            <th>Price</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        {''.join(product_rows)}
                    </tbody>
                </table>
            </div>
            {''.join(product_modals)}
        </div>
        
        <div class="admin-panel mt-4">
            <h3>Member Management</h3>
            <div class="table-responsive">
                <table class="table table-striped">
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Name</th>
                            <th>Email</th>
                            <th>Status</th>
                        </tr>
                    </thead>
                    <tbody>
                        {''.join(member_rows)}
                    </tbody>
                </table>
            </div>
        </div>
    </div>
    '''
    return render_template_string(base_template(content, "Rifat TestLabs - Admin Panel"))

@app.route('/edit_product/<int:product_id>', methods=['POST'])
@admin_required
def edit_product(product_id):
    product = next((p for p in products if p['id'] == product_id), None)
    if product:
        product['name'] = request.form.get('name')
        product['price'] = float(request.form.get('price'))
        flash('Product updated successfully!', 'success')
    return redirect('/admin_panel')

@app.route('/admin_logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
