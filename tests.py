import unittest
from app import app, db, Product

class ProductApiTestCase(unittest.TestCase):
    def setUp(self):
        # Setup test client and database
        self.app = app.test_client()
        self.app.testing = True

        # Create a fresh database for each test
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        # Clean up the database after each test
        with self.app.app_context():
            db.drop_all()

    def test_create_product(self):
        response = self.app.post('/products', json={
            'title': 'Test Product',
            'price': 10.0
        })
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertIn('id', data)

    def test_update_product(self):
        # First create a product
        response = self.app.post('/products', json={
            'title': 'Old Title',
            'price': 10.0
        })
        product = response.get_json()
        product_id = product['id']

        # Update the product
        response = self.app.put(f'/products/{product_id}', json={'title': 'New Title'})
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['title'], 'New Title')

        # Re-fetch product to ensure it's updated
        updated_product = Product.query.get(product_id)
        self.assertEqual(updated_product.title, 'New Title')

    def test_delete_product(self):
        # Create a product
        response = self.app.post('/products', json={
            'title': 'Test Product',
            'price': 10.0
        })
        product = response.get_json()
        product_id = product['id']

        # Delete the product
        response = self.app.delete(f'/products/{product_id}')
        self.assertEqual(response.status_code, 200)

        # Try to fetch the product again
        response = self.app.get(f'/products/{product_id}')
        self.assertEqual(response.status_code, 404)
        self.assertIn('error', response.get_json())
