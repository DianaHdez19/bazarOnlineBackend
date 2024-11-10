from flask import Flask, request, jsonify
from db import get_db_connection
import json
from flask_cors import CORS

app = Flask(__name__)
CORS(app) 


@app.route('/api/items', methods=['GET'])
def search_items():
    query = request.args.get('q', '')
    connection = get_db_connection() 
    cursor = connection.cursor() 
    cursor.execute("SELECT * FROM products WHERE title LIKE %s", ('%' + query + '%',))
    
    products = cursor.fetchall()
    
    product_list = []
    for product in products:
        product_dict = {
            "id": product[0],
            "title": product[1],
            "description": product[2],
            "price": float(product[3]),
            "discountPercentage": float(product[4]),
            "rating": float(product[5]),
            "stock": product[6],
            "brand": product[7],
            "category": product[8],
            "thumbnail": product[9],
            "images": json.loads(product[10])
        }
        product_list.append(product_dict)
    
    cursor.close() 
    connection.close() 
    return jsonify(product_list)


@app.route('/api/items/<int:id>', methods=['GET'])
def get_item(id):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM products WHERE id = %s", (id,))
    product = cursor.fetchone()
    cursor.close()
    connection.close()
    return jsonify(product)

@app.route('/api/addSale', methods=['POST'])
def add_sale():
    product_id = request.json.get('product_id')
    quantity = request.json.get('quantity')
    connection = get_db_connection()  
    cursor = connection.cursor() 
    cursor.execute("INSERT INTO sales (product_id, quantity) VALUES (%s, %s)", (product_id, quantity))
    connection.commit()  
    cursor.close()  
    connection.close() 
    return jsonify({"success": True})

@app.route('/api/sales', methods=['GET'])
def get_sales():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM sales")
    sales = cursor.fetchall()
    cursor.close()
    connection.close()
    return jsonify(sales)

if __name__ == '__main__':
    app.run(debug=True)
