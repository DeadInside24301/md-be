from flask_jwt_extended import (
    create_access_token, 
    jwt_required, 
    get_jwt_identity, 
)
from app.repository import UserRepository, ProductRepository, TransactionRepository
from flask import request, jsonify, make_response
from werkzeug.security import generate_password_hash, check_password_hash

class UserController:
    @staticmethod
    def register():
        data = request.get_json()
        if not data:
            return make_response(jsonify({'message': 'No input provided'}), 400)
        try:
            user_username = data['user_username']
            raw_password = data['user_password']
            user_password = generate_password_hash(raw_password, method='pbkdf2:sha256')
        except Exception as e:
            return make_response(jsonify({'message': f'Error processing fields: {str(e)}'}), 400)
        
        if UserRepository.get_user_by_username(user_username):
            return make_response(jsonify({'message': 'User already exists'}), 400)
        user = UserRepository.create_user(
            user_user_name=user_username,
            user_password=user_password,
        )
        if not user:
            return make_response(jsonify({'message': 'User creation failed'}), 500)
        return make_response(jsonify({
            'message': 'User registered successfully',
            'user': {'username': user['user_username']}
        }), 201)
    
    @staticmethod
    def login():
        data = request.get_json()
        user_username = data['user_username']
        user_password = data['user_password']
        
        user = UserRepository.get_user_by_username(user_username)
        if not user:
            return make_response(jsonify({'message': 'Account Does Not Exist'}), 404)
        if not check_password_hash(user['user_password'], user_password):
            return make_response(jsonify({'message': 'Invalid Credentials. Please Try Again'}), 401)
        
        access_token = create_access_token(identity=user_username)
        return make_response(jsonify({
            'message': 'Login successful', 
            'access_token': access_token, 
        }), 200)

class ProductController:
    @staticmethod
    def randomshit():
        return

class TransactionController:
    @staticmethod
    def randomshit():
        return
