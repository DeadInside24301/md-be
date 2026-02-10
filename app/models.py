import uuid
from sqlalchemy import Column, Text, func, DateTime
from sqlalchemy.dialects.postgresql import UUID
from app import db

class User(db.Model):
    __tablename__ = 'user_table'
    user_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_username = db.Column(db.Text, nullable=False)
    user_password = db.Column(db.Text, nullable=False)
    date_created = db.Column(db.DateTime,nullable=False, server_default=func.now())


class Product(db.Model):
    __tablename__ = 'product_table'
    product_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    product_type = db.Column(db.Text, nullable=False)
    product_sku = db.Column(db.Text, nullable=False, unique=True)
    product_quantity = db.Column(db.Integer, nullable=False)
    date_created = db.Column(db.DateTime,nullable=False, server_default=func.now())
    product_brand = db.Column(db.Text, nullable=False)
    product_size = db.Column(db.Text, nullable=False)
    product_desc = db.Column(db.Text, nullable=False)
    product_price = db.Column(db.Integer,nullable=False)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('user_table.user_id'), nullable = False)

    user = db.relationship('User', lazy='select')
class Transaction(db.Model):
    __tablename__ = 'transaction_table'
    transaction_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    product_id = db.Column(UUID(as_uuid=True), db.ForeignKey('product_table.product_id'), nullable= False)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('user_table.user_id'), nullable = False)
    transaction_type = db.Column(db.Text, nullable=False)
    transaction_quantity = db.Column(db.Integer, nullable=False)
    date_created = db.Column(db.DateTime,nullable=False, server_default=func.now())

    product = db.relationship('Product', lazy='select')
    user = db.relationship('User', lazy='select')