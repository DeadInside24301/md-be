from sqlalchemy import func, case
from app import db
from app.models import User, Product, Transaction

class UserRepository:
    @staticmethod
    def get_all_users():
        users = User.query.all()
        return [UserRepository.extract_user_data(user) for user in users]
    
    @staticmethod
    def _get_user_instance_by_username(username):
        return User.query.filter_by(user_username=username).first()
    
    @staticmethod
    def get_user_by_user_id(user_id):
        return User.query.filter_by(user_id=user_id).first()

    @staticmethod
    def get_user_by_username(username):
        user = UserRepository._get_user_instance_by_username(username)
        return UserRepository.extract_user_data(user) if user else None

    @staticmethod
    def extract_user_data(user):
        return {
            'user_id': user.user_id,
            'user_username': user.user_username,
            'user_password': user.user_password,
            'date_created': user.date_created,
        }
    @staticmethod
    def create_user(user_username, user_password):
        new_user = User(
            user_username=user_username,
            user_password=user_password,
        )
        db.session.add(new_user)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"Error creating user: {e}")
            return None
        return UserRepository.extract_user_data(new_user)


class ProductRepository:
    @staticmethod
    def extract_product_data(product):
        return {
            'product_id': product.product_id,
            'product_type': product.product_type,
            'product_sku': product.product_sku,
            'product_quantity': product.product_quantity,
            'product_price': product.product_price,
            'date_created': product.date_created,
            'product_brand': product.product_brand,
            'product_size': product.product_size,
            'product_desc': product.product_desc,
            'user_id': product.user_id,
        }

    @staticmethod
    def get_items(user_id):
        products = Product.query.filter_by(user_id=user_id).all()
        return [ProductRepository.extract_product_data(p) for p in products]

    @staticmethod
    def check_item(user_id, product_id):
        return Product.query.filter_by(user_id=user_id, product_id=product_id).first()

    @staticmethod
    def check_item_data(user_id, product_id):
        item = ProductRepository.check_item(user_id, product_id)
        return ProductRepository.extract_product_data(item) if item else None

    @staticmethod
    def get_item_sku(product_sku, user_id):
        return Product.query.filter_by(user_id=user_id, product_sku=product_sku).first()

    @staticmethod
    def delete_item(product_id):
        item = Product.query.get(product_id)
        if not item:
            return None
        db.session.delete(item)
        db.session.commit()
        return item

    @staticmethod
    def create_product(user_id, product_type, product_sku, product_quantity,
                       product_price, product_brand, product_size, product_desc):
        new_item = Product(
            user_id=user_id,
            product_type=product_type,
            product_sku=product_sku,
            product_quantity=product_quantity,
            product_price=product_price,
            product_brand=product_brand,
            product_size=product_size,
            product_desc=product_desc
        )
        db.session.add(new_item)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"Error creating product: {e}")
            return None
        return ProductRepository.extract_product_data(new_item)

    @staticmethod
    def update_item(product_id, updated_fields):
        item = Product.query.get(product_id)
        if not item:
            return None
        for field, value in updated_fields.items():
            if value is not None:
                setattr(item, field, value)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"Error updating product: {e}")
            return None
        return ProductRepository.extract_product_data(item)
        

class TransactionRepository:
    @staticmethod
    def extract_transaction_data(transaction):
        return {
            'transaction_id': transaction.transaction_id,
            'product_id': transaction.product_id,
            'user_id': transaction.user_id,
            'transaction_type': transaction.transaction_type,
            'transaction_quantity': transaction.transaction_quantity,
            'date_created': transaction.date_created,
        }

    @staticmethod
    def add_stock(product_id, quantity):
        product = Product.query.get(product_id)
        if not product:
            return None
        product.product_quantity += quantity
        try:
            db.session.commit()
            return product
        except Exception as e:
            db.session.rollback()
            print(f"Error adding stock: {e}")
            return None

    @staticmethod
    def subtract_stock(product_id, quantity):
        product = Product.query.get(product_id)
        if not product:
            return None
        if product.product_quantity < quantity:
            raise ValueError("Not enough stock")
        product.product_quantity -= quantity
        try:
            db.session.commit()
            return product
        except Exception as e:
            db.session.rollback()
            print(f"Error subtracting stock: {e}")
            return None

    @staticmethod
    def create_transaction(product_id, user_id, transaction_type, transaction_quantity):
        if transaction_type == 0:
            TransactionRepository.add_stock(product_id, transaction_quantity)
            type_label = "Move-In"
        elif transaction_type == 1:
            TransactionRepository.subtract_stock(product_id, transaction_quantity)
            type_label = "Move-Out"
        else:
            return None

        transaction = Transaction(
            product_id=product_id,
            user_id=user_id,
            transaction_type=type_label,
            transaction_quantity=transaction_quantity
        )
        db.session.add(transaction)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"Error creating transaction: {e}")
            return None
        return TransactionRepository.extract_transaction_data(transaction)

    @staticmethod
    def get_transactions(user_id):
        transactions = Transaction.query.filter_by(user_id=user_id).all()
        return [TransactionRepository.extract_transaction_data(t) for t in transactions]

    @staticmethod
    def get_barchart_data(user_id):
        return (
            db.session.query(
                Product.product_sku,
                func.sum(
                    case(
                        (Transaction.transaction_type == 'Move-In', Transaction.transaction_quantity),
                        else_=0
                    )
                ).label('total_in'),
                func.sum(
                    case(
                        (Transaction.transaction_type == 'Move-Out', Transaction.transaction_quantity),
                        else_=0
                    )
                ).label('total_out')
            )
            .outerjoin(Transaction, Transaction.product_id == Product.product_id).filter(Product.user_id == user_id)
            .group_by(Product.product_sku)
            .all()
        )