from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from security import authenticate, identity
from user import UserRegister
from items import Item, ItemList

app = Flask(__name__)
app.secret_key = 'jose'
# Api lets you add Resources, and Resource lets you define HTTP Methods for your API
api = Api(app)  
# JWT creates /auth endpoint that permits POST requests for Authentication and Identification, returns a JWT Token
# You can pass the token in the Headers E.g. Authorization = 'JWT $Token'
jwt = JWT(app, authenticate, identity)  


# Create the endpoints
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')

# Only the file that you run(python app.py) == '__main__'
if __name__ == '__main__':
    app.run(port=5000, debug=True)
