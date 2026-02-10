from flask import Blueprint, jsonify, make_response
from app.controllers import UserController, ProductController, TransactionController
from app.repository import UserRepository
from flask_jwt_extended import (
    jwt_required, get_jwt_identity,create_access_token
)
routes = Blueprint('routes', __name__)

@routes.route('/register', methods=['POST']) 
def register():
    return UserController.register()
@routes.route('/login', methods=['POST'])
def login():
    return UserController.login()
@routes.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    user_id = get_jwt_identity()
    user = UserRepository.get_user_by_user_id(user_id)
    if not user:
        return make_response(jsonify({'message': 'User not found'}), 404)
    new_access_token = create_access_token(
        identity=user["user_id"],
        additional_claims={"user_username": user["user_username"]}
    )
    return make_response(jsonify({
        'message': 'Access token refreshed successfully',
        'access_token': new_access_token
    }), 200)

@routes.route('/hello_world', methods=['GET']) 
def hello_world():
    print("Hello")
    return make_response(jsonify({
            'message': 'Backend Connected',
        }), 200)

@routes.route('/user/product', methods=['POST']) 
@jwt_required()
def add_product():
    user_id = get_jwt_identity()
    return ProductController.create_item(user_id)

@routes.route("/user/product", methods=["GET"])
@jwt_required()
def get_user_products():
    user_id = get_jwt_identity()
    print(user_id)
    return ProductController.get_items(user_id)

@routes.route("/user/product/<uuid:product_id>",methods=["PATCH"]) 
@jwt_required()
def update_product(product_id):
    user_id = get_jwt_identity()
    return ProductController.update_item(user_id,product_id)

@routes.route('/user/product/<uuid:product_id>', methods=['DELETE']) 
@jwt_required()
def delete_product(product_id):
    user_id = get_jwt_identity()
    return ProductController.delete_item(user_id,product_id)



@routes.route('/user/stock_transaction', methods=['POST'])
@jwt_required()
def stock_transaction():
    user_id = get_jwt_identity()
    return TransactionController.create_transaction(user_id)

@routes.route('/user/stock_transaction/history', methods=['GET'])
@jwt_required()
def get_transactions():
    user_id = get_jwt_identity()
    return TransactionController.get_transactions(user_id)

@routes.route('/user/stock_transaction/barchart', methods=['GET'])
@jwt_required()
def get_barchart_data():
    user_id = get_jwt_identity()
    return TransactionController.get_barchart_data(user_id)