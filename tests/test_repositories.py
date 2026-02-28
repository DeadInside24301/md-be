import pytest
from app import create_app, db
from app.models import User, Product
from app.repository import (
    UserRepository,
    ProductRepository,
    TransactionRepository
)
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
    user = UserRepository.create_user(
        user_username="repo_user",
        user_password="hashed_pass"
    )

    assert user is not None
    assert user["user_username"] == "repo_user"

    saved = session.query(User).first()
    assert saved.user_username == "repo_user"


def test_get_user_by_username(session):
    user = User(user_username="lookup_user", user_password="pass")
    session.add(user)
    session.commit()

    result = UserRepository.get_user_by_username("lookup_user")

    assert result is not None
    assert result["user_username"] == "lookup_user"

def create_test_user(session):
    user = User(user_username="owner", user_password="pass")
    session.add(user)
    session.commit()
    return user

def test_create_product(session):
    user = create_test_user(session)

    product = ProductRepository.create_product(
        user_id=user.user_id,
        product_type="Electronics",
        product_sku="SONY-TV-42",
        product_quantity=5,
        product_price=10000,
        product_brand="Sony",
        product_size="42",
        product_desc="Television"
    )

    assert product is not None
    assert product["product_sku"] == "SONY-TV-42"

def test_get_items_by_user(session):
    user = create_test_user(session)

    ProductRepository.create_product(
        user_id=user.user_id,
        product_type="Item",
        product_sku="SKU1",
        product_quantity=5,
        product_price=100,
        product_brand="Brand",
        product_size="M",
        product_desc="Desc"
    )

    items = ProductRepository.get_items(user.user_id)

    assert len(items) == 1
    assert items[0]["product_sku"] == "SKU1"

def test_update_item(session):
    user = create_test_user(session)

    product = ProductRepository.create_product(
        user_id=user.user_id,
        product_type="Item",
        product_sku="SKU2",
        product_quantity=5,
        product_price=100,
        product_brand="Brand",
        product_size="M",
        product_desc="Desc"
    )

    ProductRepository.update_item(
        product["product_id"],
        {"product_quantity": 10}
    )

    updated = session.query(Product).first()
    assert updated.product_quantity == 10

def test_delete_item(session):
    user = create_test_user(session)

    product = ProductRepository.create_product(
        user_id=user.user_id,
        product_type="Item",
        product_sku="SKU3",
        product_quantity=5,
        product_price=100,
        product_brand="Brand",
        product_size="M",
        product_desc="Desc"
    )

    ProductRepository.delete_item(product["product_id"])

    remaining = session.query(Product).all()
    assert len(remaining) == 0


def test_add_stock(session):
    user = create_test_user(session)

    product = ProductRepository.create_product(
        user_id=user.user_id,
        product_type="Item",
        product_sku="SKU4",
        product_quantity=5,
        product_price=100,
        product_brand="Brand",
        product_size="M",
        product_desc="Desc"
    )

    TransactionRepository.add_stock(product["product_id"], 5)

    updated = session.query(Product).first()
    assert updated.product_quantity == 10

def test_subtract_stock_success(session):
    user = create_test_user(session)

    product = ProductRepository.create_product(
        user_id=user.user_id,
        product_type="Item",
        product_sku="SKU5",
        product_quantity=10,
        product_price=100,
        product_brand="Brand",
        product_size="M",
        product_desc="Desc"
    )

    TransactionRepository.subtract_stock(product["product_id"], 5)

    updated = session.query(Product).first()
    assert updated.product_quantity == 5

def test_subtract_stock_not_enough(session):
    user = create_test_user(session)

    product = ProductRepository.create_product(
        user_id=user.user_id,
        product_type="Item",
        product_sku="SKU6",
        product_quantity=3,
        product_price=100,
        product_brand="Brand",
        product_size="M",
        product_desc="Desc"
    )

    with pytest.raises(ValueError):
        TransactionRepository.subtract_stock(product["product_id"], 10)

def test_create_transaction_move_out(session):
    user = create_test_user(session)

    product = ProductRepository.create_product(
        user_id=user.user_id,
        product_type="Item",
        product_sku="SKU8",
        product_quantity=10,
        product_price=100,
        product_brand="Brand",
        product_size="M",
        product_desc="Desc"
    )

    TransactionRepository.create_transaction(
        product_id=product["product_id"],
        user_id=user.user_id,
        transaction_type=1,
        transaction_quantity=4
    )

    updated = session.query(Product).first()
    assert updated.product_quantity == 6
