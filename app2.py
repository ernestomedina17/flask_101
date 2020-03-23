#!/usr/local/bin/python3.7
from flask import Flask
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

    def post(self, name):
        item = {'name': name, 'price': 12.00}
        items.append(item)
        return item, 201  # Created, 202 is Accepted but still creating it may take a long time

api.add_resource(Item, '/item/<string:name>')

app.run(port=5000)
