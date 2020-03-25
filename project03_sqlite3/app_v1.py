from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required
from security import authenticate, identity
from user import UserRegister

app = Flask(__name__)
app.secret_key = 'jose'
# Api lets you add Resources, and Resource lets you define HTTP Methods for your API
api = Api(app)  
# JWT creates /auth endpoint that permits POST requests for Authentication and Identification, returns a JWT Token
# You can pass the token in the Headers E.g. Authorization = 'JWT $Token'
jwt = JWT(app, authenticate, identity)  
# List of dictionaries to hold the items, E.g. 
#   "items": [
#       {
#           "name": "pencil",
#           "price": 1.99
#       },
#       {
#           "name": "piano",
#           "price": 5.9
#       }
#   ]
items = []  


class Item(Resource):
    # Gets the Request so you can parse it for validation
    parser = reqparse.RequestParser() 
    # The 'price' argument is required in the request
    parser.add_argument('price',
                        type=float,
                        required=True,  
                        help="This field cannot be left blank!")

    # This is a DECORATOR that wrapps this GET HTTP Request Method to enforce Authorization via JWT Token in the Header
    @jwt_required()
    # GET HTTP Method to retrieve an item from the List
    # http://localhost:5000/item/<string:name>
    def get(self, name):
        # next(iterator[, default]) - fetch next item from the collection, returns an Element, If no item is present returns None by default
        # filter (function, iterable) - returns the same as returned by the function, iterates over items[] which contains {} elements
        # the lambda returns 'x' which is a dictionary object that represents an item that matches the name of the item within the 'items' list
        item = next(filter(lambda x: x['name'] == name, items), None)
        # Returns a JSON object or Python dictionary, with the Key 'item' and value another Dictionary, E.g.
        # { "item": { "name": "piano", "price": 5.9 } }
        # Response Status code is 200 (OK), otherwise 404 (Not found)
        return {'item': item}, 200 if item else 404  

    # POST HTTP Method to append another item into the List.
    # http://localhost:5000/item/<string:name>
    def post(self, name):
        # If there is an item with that 'name', do not creaet it, and return a Response Status code of 400 (Bad Request)
        if next(filter(lambda x: x['name'] == name, items), None):
            return {'message': "An item with name '{}' already exists".format(name)}, 400

        # Get the request and make sure it includes the 'price'
        data = self.parser.parse_args()
        item = {'name': name, 'price': data['price']}
        items.append(item)
        # 201 (Created)
        return item, 201  

    # DELETE HTTP Method to delete an item from the List
    # http://localhost:5000/item/<string:name>
    def delete(self, name):
        # Don't want to create a local variable in this space
        global items
        # Updates the items List where only elements that don't have the name of the item that we want to delete will remain
        items = list(filter(lambda x: x['name'] != name, items))
        return {'message': "Item('{}') deleted".format(name)}

    # PUT HTTP Method to update an existing item or append a new item into the List
    # http://localhost:5000/item/<string:name>
    def put(self, name):
        data = self.parser.parse_args()
        item = next(filter(lambda x: x['name'] == name, items), None)
        if item is None:
            item = {'name': name, 'price': data['price']}
            items.append(item)
        else:
            item.update(data)
        return item


class ItemList(Resource):
    # GET HTTP Method to return the list of items as a JSON or Python Dictionary with they Key items
    def get(self):
        return {'items': items}

# Create the endpoints
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')

app.run(port=5000, debug=True)
