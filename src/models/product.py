from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost/productos_prueba'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

class Product(db.Model):
    __tablename__ = "products"
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(50))
    productDescription = db.Column(db.String(150))
    productBrand = db.Column(db.String(50))
    price = db.Column(db.Float)

    
    def __init__(self, title, productDescription, productBrand, price):
        self.title = title
        self.productDescription = productDescription
        self.productBrand = productBrand
        self.price = price

db.create_all()

class ProductSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'productDescription', 'productBrand', 'price')

product_schema = ProductSchema()

@app.route('/products', methods = ['POST'])
def createProduct():
    response = request.get_json()

    for i in response:
        title = i['title'];
        productDescription = i['productDescription'];
        productBrand = i['productBrand'];
        price = i['price'];

        new_product = Product(title, productDescription, productBrand, price)
        db.session.add(new_product)
        db.session.commit()

    print(response[0]['title'])

    if response[0]['title'] == 'Título 1':
        print('Logged in')
    else:
        print('Incorrect credentials')

    return 'Producto(s) insertado(s) correctamente'

@app.route('/products', methods = ['GET'])
def getProduct():
    get_products = Product.query.all()
    product_schema = ProductSchema(many = True)
    products = product_schema.dump(get_products)

    return make_response(jsonify({"products": products}))

@app.route('/products/<id>', methods = ['GET'])
def getProductByID(id):
    get_product = Product.query.get(id)
    product_schema = ProductSchema()
    product = product_schema.dump(get_product)

    return make_response(jsonify({"product": product}))

@app.route('/products/<id>', methods=['PUT'])
def updateProduct(id):
    data = request.json()
    get_product = Product.query.get(id)

    print(data)

    if data.get('title'):
        get_product.title = data['title']

    if data.get('productDescription'):
        get_product.productDescription = data['productDescription']

    if data.get('productBrand'):
        get_product.productBrand = data['productBrand']

    if data.get('price'):
        get_product.price= data['price']

    db.session.add(get_product)
    db.session.commit()

    product_schema = ProductSchema(only=['id', 'title', 'productDescription','productBrand','price'])
    product = product_schema.dump(get_product)

    return make_response(jsonify({"product": product}))

@app.route('/products/<id>', methods = ['DELETE'])
def deleteProduct(id):
    get_product = Product.query.get(id)
    db.session.delete(get_product)
    db.session.commit()

    return make_response("",204)
@app.route('/products', methods = ['POST'])

if __name__ == "__main__":
    app.run(debug=True)