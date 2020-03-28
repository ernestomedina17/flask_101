import os
from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from security import authenticate, identity
from db import db
from resources.user import UserRegister, User, UserLogin, TokenRefresh
from resources.item import Item, ItemList
from resources.store import Store, StoreList

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
# Turns Off Flask Obj mod tracking, cause the one in SqlAlchemy is better
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.secret_key = 'jose'  # app.config['JWT_SECRET_KEY']
# Api lets you add Resources, and Resource lets you define HTTP Methods for your API
api = Api(app)  

@app.before_first_request
def create_tables():
    db.create_all()

# JWT Extended
jwt = JWTManager(app)  # Does not create the /auth 

# Refresh token
@jwt.user_claims_loader
def add claims_to_jwt(identity):  # user.id
    if identity == 1:   # read from DB or config file instead of hardcoding
        return {'is_admin': True}
    return {'is_admin': False}

# Message sent when you are required to re-authenticate (fresh)
@jwt.expired_token_loader
def expired_token_callback():
    return jsonify({
        'description': 'The token has expired.',
        'error': 'token_expired'
    }), 401

@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({
        'description': 'Signature verification failed.',
        'error': 'invalid_token'
    }), 401

@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify({
        'description': 'Request does not contain an access token.',
        'error': 'authorization_required'
    }), 401

@jwt.needs_fresh_token_loader
def token_not_fresh_callback():
    return jsonify({
        'description': 'The token is not fresh',
        'error': 'fresh_token_required'
    }), 401

@jwt.revoked_token_loader
def revoked_token_callback():
    return jsonify({
        'description': 'The token has been revoked.',
        'error': 'token_revoked'
    }), 401


# Create the endpoints
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')
# api.add_resource(User, '/user/<int:user_id>')
# Instead of /auth, it returns access_token and refresh Token
# In Postman Auth Header use Bearer {{token}} instead of JWT {{token}}
api.add_resource(UserLogin, '/login') 
api.add_resource(TokenRefresh, '/refresh') 

db.init_app(app)
# Heroku uses uWSGI instead of Flask hence we comment out the below line
# app.run(port=5000, debug=True)



