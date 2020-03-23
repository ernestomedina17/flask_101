#!/usr/local/bin/python3.7
from flask import Flask, request
from flask_restful import Resource, Api
from flask_jwt import JWT, jwt_required
from security import authenticate, identity


app = Flask(__name__)
app.secret_key = 'jose'
api = Api(app)  # no need for jsonify anymore

jwt = JWT(app, authenticate, identity)  # /auth endpoint- authenticate=username, identity=id

items = []  # in memory DB


class Item(Resource):
    @jwt_required()       # DECORATOR - Requires Authorization JWT Token in the Header
    def get(self, name):
        item = next(filter(lambda x: x['name'] == name, items), None)  # If no next item, then None
        return {'item': item}, 200 if item else 404  # if item exists 200, if not 404 not found

    def post(self, name):
        if next(filter(lambda x: x['name'] == name, items), None):
            return {'message': "An item with name '{}' already exists".format(name)}, 400

        data = request.get_json()  # (force=True) don't look at the header, #(silent=True) returns None
        item = {'name': name, 'price': data['price']}
        items.append(item)
        return item, 201  # Created, 202 is Accepted but still creating it may take a long time

    def delete(self, name):
        global items
        items = list(filter(lambda x: x['name'] != name, items))  # filter is like grep
        return {'message': "Item('{}') deleted".format(name)}

    def put(self, name):  # UPDATE
        data = request.get_json()
        item = next(filter(lambda x: x['name'] == name, items), None)
        if item is None:
            item = {'name': name, 'price': data['price']}
            items.append(item)
        else:
            item.update(data)
        return item

class ItemList(Resource):
    def get(self):
        return {'items': items}


api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')

app.run(port=5000, debug=True)
