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
    def get_user_by_username(username):
        user = UserRepository._get_user_instance_by_username(username)
        return UserRepository.extract_user_data(user) if user else None

    @staticmethod
    def extract_user_data(user):
        return {
            'user_id': user.user_id,
            'user_user_name': user.user_username,
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
    def randomshit():
        return

class TransactionRepository():
    @staticmethod
    def randomshit():
        return