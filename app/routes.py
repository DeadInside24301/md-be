from flask import Blueprint
from app.controllers import UserController
from flask_jwt_extended import (
    jwt_required, 
    get_jwt_identity, 
)
routes = Blueprint('routes', __name__)

routes.route('/register', methods=['POST'])(UserController.register)
routes.route('/login', methods=['POST'])(UserController.login)