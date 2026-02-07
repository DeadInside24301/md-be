from flask import Blueprint, jsonify, make_response
from app.controllers import UserController
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

@routes.route("/user/products", methods=["GET"])
@jwt_required()
def get_user_products():
    return

@routes.route("/user/products-data",methods=["GET"])
@jwt_required()
def get_user_product_data():
    return