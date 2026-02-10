from flask import Blueprint, jsonify, make_response
from app.controllers import UserController, ProductController, TransactionController
from flask_jwt_extended import (
    jwt_required, 
    get_jwt_identity, 
)
routes = Blueprint('routes', __name__)

@routes.route('/register', methods=['POST'])
def register():
    return UserController.register()
@routes.route('/login', methods=['POST'])
def login():
    return UserController.login()

@routes.route('/hello_world', methods=['GET'])
def hello_world():
    print("Hello") # this gets executed
    return make_response(jsonify({
            'message': 'Backend Connected',
        }), 200)

@routes.route('/user/product', methods=['POST']) #C
@jwt_required()
def add_product():
    return ProductController.create_item()

@routes.route("/user/product", methods=["GET"]) #R
@jwt_required()
def get_user_products():
    return ProductController.get_items()

@routes.route("/user/product/<uuid:product_id>",methods=["PATCH"]) #U
@jwt_required()
def update_product(product_id):
    return ProductController.update_item(product_id)

@routes.route('/user/product/<uuid:product_id>', methods=['DELETE']) #D
@jwt_required()
def delete_product(product_id):
    return ProductController.delete_item(product_id)



@routes.route('/user/stock_transaction', methods=['POST'])
@jwt_required()
def stock_transaction():
    return TransactionController.create_transaction()

@routes.route('/user/stock_transaction/history', methods=['GET'])
@jwt_required()
def get_transactions():
    return TransactionController.get_transactions()

@routes.route('/user/stock_transaction/barchart', methods=['GET'])
@jwt_required()
def get_transactions():
    return TransactionController.get_barchart_data()