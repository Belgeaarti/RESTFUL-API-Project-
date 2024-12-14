from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///products.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define the Product model
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    price = db.Column(db.Float, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'price': self.price
        }

# Initialize the database
with app.app_context():
    db.create_all()

# Routes

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        'message': 'Welcome to the Product API!',
        'endpoints': {
            'GET /products': 'Retrieve all products',
            'POST /products': 'Create a new product',
            'GET /products/<id>': 'Retrieve a specific product by ID',
            'PUT /products/<id>': 'Update a specific product by ID',
            'DELETE /products/<id>': 'Delete a specific product by ID'
        }
    })

@app.route('/favicon.ico', methods=['GET'])
def favicon():
    return '', 204

@app.route('/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    return jsonify([product.to_dict() for product in products])

@app.route('/products/<int:id>', methods=['GET'])
def get_product(id):
    product = Product.query.get(id)
    if product is None:
        return jsonify({'error': 'Product not found'}), 404
    return jsonify(product.to_dict())

@app.route('/products', methods=['POST'])
def create_product():
    data = request.get_json()
    if not data or 'title' not in data or 'price' not in data:
        return jsonify({'error': 'Invalid data'}), 400

    new_product = Product(
        title=data['title'],
        description=data.get('description', ''),
        price=data['price']
    )
    db.session.add(new_product)
    db.session.commit()
    return jsonify(new_product.to_dict()), 201

@app.route('/products/<int:id>', methods=['PUT'])
def update_product(id):
    product = Product.query.get(id)
    if product is None:
        return jsonify({'error': 'Product not found'}), 404

    data = request.get_json()
    if not data:
        return jsonify({'error': 'Invalid data'}), 400

    product.title = data.get('title', product.title)
    product.description = data.get('description', product.description)
    product.price = data.get('price', product.price)

    db.session.commit()  # Commit changes
    db.session.refresh(product)  # Refresh the product to rebind it to the session

    return jsonify(product.to_dict())

# DELETE route to delete a product
@app.route('/products/<int:id>', methods=['DELETE'])
def delete_product(id):
    # Get the product by ID
    product = Product.query.get(id)
    if product is None:
        return jsonify({'error': 'Product not found'}), 404

    # Delete the product
    db.session.delete(product)
    db.session.commit()

    return jsonify({'message': 'Product deleted successfully'}), 200

# Error handling
@app.errorhandler(404)
def not_found(e):
    return jsonify({'error': 'Resource not found'}), 404

@app.errorhandler(500)
def server_error(e):
    return jsonify({'error': 'Internal server error'}), 500

# Unit Tests (for testing purposes)
if __name__ == '__main__':
    app.run(debug=True)
