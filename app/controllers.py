from flask_jwt_extended import (
    create_access_token,
    create_refresh_token 
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
            refresh_token = create_refresh_token(identity=user["user_id"],additional_claims={"user_username": user["user_username"]})
        return make_response(jsonify({
            'message': 'Login successful', 
            'access_token': access_token, 
            'refresh_token':refresh_token
        }), 200)

class ProductController:

    @staticmethod
    def get_items(user_id):
        items = ProductRepository.get_items(user_id)
        return make_response(jsonify({'Products':items}), 200)

    @staticmethod
    def create_item(user_id):
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
        except KeyError as e:
            return make_response(jsonify({'message': f'Missing field: {e}'}), 400)

        product_sku = f"{product_brand}-{product_type}-{product_size}".upper()

        if ProductRepository.get_item_sku(product_sku, user_id):
            return make_response(jsonify({'message': 'Product already exists'}), 400)

        item = ProductRepository.create_product(
            user_id=user_id,
            product_type=product_type,
            product_sku=product_sku,
            product_quantity=product_quantity,
            product_price=product_price,
            product_brand=product_brand,
            product_size=product_size,
            product_desc=product_desc
        )

        return make_response(jsonify({
            'message': 'Product created successfully',
            'product': item
        }), 201)

    @staticmethod
    def update_item(user_id, product_id):
        data = request.get_json()
        item = ProductRepository.check_item_data(user_id, product_id)

        if not item:
            return make_response(jsonify({'message': 'Item not found'}), 404)

        updated_fields = {
            'product_type': data.get('product_type', item['product_type']),
            'product_quantity': data.get('product_quantity', item['product_quantity']),
            'product_price': data.get('product_price', item['product_price']),
            'product_brand': data.get('product_brand', item['product_brand']),
            'product_size': data.get('product_size', item['product_size']),
            'product_desc': data.get('product_desc', item['product_desc']),
        }

        ProductRepository.update_item(product_id, updated_fields)
        return make_response(jsonify({'message': 'Product updated successfully'}), 200)

    @staticmethod
    def delete_item(user_id, product_id):
        item = ProductRepository.check_item(user_id, product_id)
        if not item:
            return make_response(jsonify({'message': 'Item not found'}), 404)

        ProductRepository.delete_item(product_id)
        return make_response(jsonify({'message': 'Product deleted successfully'}), 200)


class TransactionController:

    @staticmethod
    def create_transaction(user_id):
        data = request.get_json()
        if not data:
            return make_response(jsonify({'message': 'No input provided'}), 400)

        try:
            product_id = data['product_id']
            transaction_type = data['transaction_type']
            transaction_quantity = data['transaction_quantity']
        except KeyError as e:
            return make_response(jsonify({'message': f'Missing field: {e}'}), 400)

        product = ProductRepository.check_item(user_id, product_id)
        if not product:
            return make_response(jsonify({'message': 'Unauthorized product access'}), 403)

        transaction = TransactionRepository.create_transaction(
            product_id=product_id,
            user_id=user_id,
            transaction_type=transaction_type,
            transaction_quantity=transaction_quantity
        )

        return make_response(jsonify({
            'message': 'Transaction successful',
            'transaction': transaction
        }), 201)

    @staticmethod
    def get_transactions(user_id):
        transactions = TransactionRepository.get_transactions(user_id)
        return make_response(jsonify({'transactions':transactions}), 200)

    @staticmethod
    def get_barchart_data(user_id):
        rows = TransactionRepository.get_barchart_data(user_id)
        items = []
        in_data = []
        out_data = []
        for row in rows:
            items.append(row.product_sku)
            in_data.append(row.total_in)
            out_data.append(row.total_out)
        return make_response(jsonify({'items': items, "in_data": in_data, "out_data": out_data}))