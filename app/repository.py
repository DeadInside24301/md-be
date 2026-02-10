from sqlalchemy import func, case
from app import db
from app.models import User, Product, Transaction

class UserRepository:
    @staticmethod
    #soon to be get_all_products -Angelo
    def get_all_users():
        users = User.query.all()
        return [UserRepository.extract_user_data(user) for user in users]
    
    @staticmethod
    def _get_user_instance_by_username(username):
        return User.query.filter_by(user_username=username).first()

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


class ProductRepository():
    @staticmethod
    def extract_product_data(product):
        return {
            'product_id': product.product_id,
            'product_type': product.product_type,
            'product_sku': product.product_sku,
            'product_quantity': product.product_quantity,
            'product_price': product.product_price,
            'date_creatd':product.date_created,
            'product_brand': product.product_brand,
            'product_size': product.product_size,
            'product_desc': product.product_desc,
        }
    @staticmethod
    def get_items():
        products = Product.query.all()
        return [ProductRepository.extract_product_data(product) for product in products]
    
    @staticmethod
    def check_item(product_id):
        return db.session.query(Product).filter_by(product_id=product_id).first()
    
    @staticmethod
    def check_item_data(product_id):
        item = Product.query.filter_by(product_id=product_id).first()
        return ProductRepository.extract_product_data(item) if item else None

    @staticmethod
    def get_item_id(product_sku):
        return db.session.query(Product.product_id).filter_by(product_sku=product_sku).first()
    
    @staticmethod
    def get_item_sku(product_sku):
        return db.session.query(Product).filter_by(product_sku=product_sku).first()
        
    @staticmethod
    def delete_item(product_id):
        item = Product.query.get(product_id)
        if not item:
            return None
        db.session.delete(item)
        db.session.commit()
        return item
    
    @staticmethod
    def create_product(product_type,product_sku,product_quantity,product_price,product_brand,product_size,product_desc):
        new_item = Product(
            product_type = product_type,
            product_sku = product_sku,
            product_quantity = product_quantity,
            product_price = product_price,
            product_brand =product_brand,
            product_size = product_size,
            product_desc = product_desc
        )
        db.session.add(new_item)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"Error creating user: {e}")
            return None
        return ProductRepository.extract_product_data(new_item)
    
    @staticmethod
    def update_item(product_id,updated_fields):
        item = ProductRepository.check_item(product_id)
        if not item:
            return None
        for field, value in updated_fields.items():
            if value is not None:
                setattr(item, field, value)
        try:
            db.session.commit()
            return ProductRepository.extract_product_data(item)
        except Exception as e:
            db.session.rollback()
            print(f"Error updating user: {e}")
            return None
        

class TransactionRepository():
    @staticmethod
    def extract_transaction_data(transaction):
        return {
            'transaction_id':transaction.transaction_id,
            'product_id': transaction.product_id,
            'user_id': transaction.user_id,
            'transaction_type': transaction.transaction_type,
            'transaction_quantity': transaction.transaction_quantity,
            'date_creatd':transaction.date_created,
        }
    @staticmethod
    def add_stock(product_id,transaction_quantity):
        product = ProductRepository.check_item(product_id)
        if not product:
            return None
        product.product_quantity += transaction_quantity
        try:
            db.session.commit()
            return product
        except Exception as e:
            db.session.rollback()
            print(f"Error adding stocks: {e}")
        return None
    
    @staticmethod
    def subtract_stock(product_id,transaction_quantity):
        product = ProductRepository.check_item(product_id)
        if not product:
            return None
        if product.product_quantity < transaction_quantity:
            print(f"Not enough  in stocks")
        product.product_quantity -= transaction_quantity
        try:
            db.session.commit()
            return product
        except Exception as e:
            db.session.rollback()
            print(f"Error adding stocks: {e}")
        return None
    
    @staticmethod
    def create_transaction(product_id,user_id,transaction_type,transaction_quantity):
        new_transaction_type = ''
        if transaction_type == 0:
            TransactionRepository.add_stock(product_id,transaction_quantity)
            new_transaction_type = "Move-In"
        if transaction_type == 1:
            TransactionRepository.subtract_stock(product_id,transaction_quantity)
            new_transaction_type = "Move-Out"
        transaction_type = new_transaction_type
        new_transaction = Transaction(
            product_id = product_id,
            user_id = user_id,
            transaction_type = transaction_type,
            transaction_quantity = transaction_quantity,
        )
        db.session.add(new_transaction)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"Error creating user: {e}")
            return None
        return TransactionRepository.extract_transaction_data(new_transaction)
    
    @staticmethod
    def get_transactions():
        transactions = Transaction.query.all()
        return [TransactionRepository.extract_transaction_data(transaction) for transaction in transactions]
    

    @staticmethod
    def get_barchart_data():
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
            .outerjoin(Transaction, Transaction.product_id == Product.product_id)
            .group_by(Product.product_sku)
            .all()
        )