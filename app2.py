#!/usr/local/bin/python3.7
from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app) # no need for jsonify anymore

items = []  # in memory DB


class Item(Resource):
    def get(self, name):
        for item in items:
            if item['name'] == name:
                return item
        return {'item': None}, 404 # not found

    def post(self, name):         #(silent=True) returns None
        data = request.get_json() #(force=True) When content type is not set, don't look at the header
        item = {'name': name, 'price': data['price']}
        items.append(item)
        return item, 201  # Created, 202 is Accepted but still creating it may take a long time


class ItemList(Resource):
    def get(self):
        return {'items': items}


api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')

app.run(port=5000, debug=True)
