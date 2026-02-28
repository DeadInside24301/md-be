import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

db = SQLAlchemy()
jwt = JWTManager()

def create_app(test_config=None):
    app = Flask(__name__)
    if test_config:
        app.config.update(test_config)
    else:

        app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DB_URL')
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        app.config['JWT_SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY')
        app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=60)

    db.init_app(app)
    jwt.init_app(app)
    CORS(app, resources={r"/*": {"origins": os.getenv('FE_URL')}})

    from app.routes import routes
    
    app.register_blueprint(routes, url_prefix="/auth")

    return app

