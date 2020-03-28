import os
from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from security import authenticate, identity
from db import db
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
# Turns Off Flask Obj mod tracking, cause the one in SqlAlchemy is better
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.secret_key = 'jose'
# Api lets you add Resources, and Resource lets you define HTTP Methods for your API
api = Api(app)  

@app.before_first_request
def create_tables():
    db.create_all()

# JWT creates /auth endpoint that permits POST requests for Authentication and Identification, returns a JWT Token
# You can pass the token in the Headers E.g. Authorization = 'JWT $Token'
jwt = JWT(app, authenticate, identity)  


# Create the endpoints
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')

db.init_app(app)
# Heroku uses uWSGI instead of Flask hence we comment out the below line
# app.run(port=5000, debug=True)

