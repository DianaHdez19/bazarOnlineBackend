import pymysql
import json

def get_db_connection():
    connection = pymysql.connect(
        host='localhost',
        user='root', 
        password='1234',  
        database='ecommerce'
    )
    return connection

with open('./products.json', 'r') as file:
    data = json.load(file)

products = data['products']

connection = get_db_connection()

try:
    with connection.cursor() as cursor:
        for product in products:
            sql = '''
                INSERT INTO products (title, description, price, discountPercentage, 
                                      rating, stock, brand, category, thumbnail, images)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            '''

            values = (
                product['title'],
                product['description'],
                product['price'],
                product['discountPercentage'],
                product['rating'],
                product['stock'],
                product['brand'],
                product['category'],
                product['thumbnail'],
                json.dumps(product['images']) 
            )

            cursor.execute(sql, values)

        connection.commit()
        print(f'{len(products)} productos insertados correctamente.')

except Exception as e:
    print(f'Error al insertar productos: {e}')
    connection.rollback()

finally:
    connection.close()
