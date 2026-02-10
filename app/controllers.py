from flask_jwt_extended import (
    create_access_token, 
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
            user_username=user_username,
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
        else:
            access_token = create_access_token(identity=user["user_id"],additional_claims={"user_username": user["user_username"]})
        return make_response(jsonify({
            'message': 'Login successful', 
            'access_token': access_token, 
        }), 200)

class ProductController:
    @staticmethod
    def get_items():
        items = ProductRepository.get_items()
        return make_response(jsonify({'Products': items}), 200)

    @staticmethod
    def delete_item(product_id):
        item_id = ProductRepository.check_item(product_id)
        if not item_id:
            return make_response(jsonify({'message': 'Item Not Found'}), 404)
        item_id = ProductRepository.delete_item(product_id)
        return make_response(jsonify({'message': 'Employee Deleted Successfully'}),200)

    @staticmethod
    def create_item():
        data = request.get_json()
        if not data:
            return make_response(jsonify({'message': 'No input provided'}), 400)
        try:
            product_type = data['product_type']
            product_quantity = data['product_quantity']
            product_price = data['product_price']
            product_brand = data['product_brand']
            product_size = data['product_size']
            product_desc = data['product_desc']
        except Exception as e:
            return make_response(jsonify({'message': f'Error processing fields: {str(e)}'}), 400)
        product_sku = f"{product_brand}-{product_type}-{product_size}".upper()
        if ProductRepository.get_item_sku(product_sku):
            return make_response(jsonify({'message': 'Product already exists'}), 400)
        item = ProductRepository.create_product(
            product_type = product_type,
            product_sku = product_sku,
            product_quantity = product_quantity,
            product_price = product_price,
            product_brand =product_brand,
            product_size = product_size,
            product_desc = product_desc
        )
        if not item:
            return make_response(jsonify({'message': 'User creation failed'}), 500)
        return make_response(jsonify({
            'message': 'Product registered successfully',
            'user': {'product': item['product_sku']}
        }), 201)
    
    @staticmethod
    def update_item(product_id):
        data = request.get_json()
        item = ProductRepository.check_item_data(product_id)
        if not item:
            return make_response(jsonify({'message': 'Item Not Found'}), 404)
        updated_fields = {
            'product_type': data.get('product_type', item['product_type']),
            'product_quantity': data.get('product_quantity', item['product_quantity']),
            'product_price': data.get('product_price', item['product_price']),
            'product_brand': data.get('product_brand', item['product_brand']),
            'product_size': data.get('product_size', item['product_size']),
            'product_desc': data.get('product_desc', item['product_desc']),
        }
        updated_item = ProductRepository.update_item(product_id, updated_fields)
        if updated_item:
            return make_response(jsonify({'message': 'Product information updated successfully'}), 200)
        return make_response(jsonify({'message': 'Update failed'}), 500)


class TransactionController:

    @staticmethod
    def create_transaction():
        data = request.get_json()
        if not data:
            return make_response(jsonify({'message': 'No input provided'}), 400)
        try:
            product_id = data['product_id']
            user_id = data['user_id']
            transaction_type = data['transaction_type']
            transaction_quantity = data['transaction_quantity']
        except Exception as e:
            return make_response(jsonify({'message': f'Error processing fields: {str(e)}'}), 400)
        transaction = TransactionRepository.create_transaction(
            product_id =product_id,
            user_id=user_id,
            transaction_type = transaction_type,
            transaction_quantity = transaction_quantity
        )
        if not transaction:
            return make_response(jsonify({'message': 'User creation failed'}), 500)
        return make_response(jsonify({
            'message': 'Product registered successfully',
            'user': {'transaction': transaction['transaction_sku']}
        }), 201)

    @staticmethod
    def get_transactions():
        transaction = TransactionRepository.get_transactions()
        return make_response(jsonify({'transactions': transaction}), 200)
    
    @staticmethod
    def get_barchart_data():
        rows = TransactionRepository.get_barchart_data()
        items = []
        in_data = []
        out_data = []
        for row in rows:
            items.append(row.product_sku)
            in_data.append(row.total_in)
            out_data.append(row.total_out)
        return make_response(jsonify({'items': items, "in_data": in_data, "out_data": out_data}))