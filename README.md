# RESTFUL-API-Project-


For running the application
:- python app.py

For testing the application
:- python .\tests.py

For posting a product
:- curl -X POST http://127.0.0.1:5000/products -H "Content-Type: application/json" -d "{\"title\": \"Test Product\", \"price\": 10.0}

For deleting a product
:- curl -X DELETE http://127.0.0.1:5000/products/1

For getting a product
:- curl -X GET http://127.0.0.1:5000/products/2

For updating a product
:-  curl -X PUT http://127.0.0.1:5000/products/2 -H "Content-Type: application/json" -d '{"title": "Updated Product", "description": "Updated description", "price": 20.0}'
 
