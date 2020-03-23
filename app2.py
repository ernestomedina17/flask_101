#!/usr/local/bin/python3.7
from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app) # no need for jsonify anymore

items = []  # in memory DB


class Item(Resource):
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


class ItemList(Resource):
    def get(self):
        return {'items': items}


api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')

app.run(port=5000, debug=True)
