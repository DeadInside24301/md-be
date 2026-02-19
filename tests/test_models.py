import pytest
from app import create_app, db
from app.models import User, Product, Transaction
import uuid


@pytest.fixture
def app():
    app = create_app()
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def session(app):
    return db.session

def test_create_user(session):
    user = User(
        user_username="testuser",
        user_password="hashedpassword"
    )

    session.add(user)
    session.commit()

    saved_user = session.query(User).first()

    assert saved_user.user_username == "testuser"
    assert saved_user.user_id is not None
    assert saved_user.date_created is not None


def test_create_product_with_user(session):
    user = User(
        user_username="owner",
        user_password="pass"
    )
    session.add(user)
    session.commit()

    product = Product(
        product_type="Electronics",
        product_sku="SKU123",
        product_quantity=10,
        product_brand="Sony",
        product_size="Medium",
        product_desc="Headphones",
        product_price=5000,
        user_id=user.user_id
    )

    session.add(product)
    session.commit()

    saved_product = session.query(Product).first()

    assert saved_product.user.user_username == "owner"


def test_create_transaction(session):
    user = User(
        user_username="buyer",
        user_password="pass"
    )
    session.add(user)
    session.commit()

    product = Product(
        product_type="Electronics",
        product_sku="SKU999",
        product_quantity=5,
        product_brand="LG",
        product_size="Large",
        product_desc="Monitor",
        product_price=8000,
        user_id=user.user_id
    )
    session.add(product)
    session.commit()

    transaction = Transaction(
        product_id=product.product_id,
        user_id=user.user_id,
        transaction_type="IN",
        transaction_quantity=3
    )

    session.add(transaction)
    session.commit()

    saved_tx = session.query(Transaction).first()

    assert saved_tx.product.product_sku == "SKU999"
    assert saved_tx.user.user_username == "buyer"
