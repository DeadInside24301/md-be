import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from app.routes import routes
from dotenv import load_dotenv

load_dotenv()

db = SQLAlchemy()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DB_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY')

    db.init_app(app)
    jwt = JWTManager(app)
    CORS(app, resources={r"/*": {"origins": os.getenv('FE_URL')}})
    app.register_blueprint(routes, url_prefix="/auth")

    return app

