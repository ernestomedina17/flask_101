#!/usr/local/bin/python3.7
from flask import Flask, jsonify, request  # jsonify in lower case because its a method

# JSON is a Python's Dictionary text/string 
stores = [
    {
        'Name': 'My Wonderful Store',
        'Items': [
            {
                'Name': 'My item',
                'Price': 15.99
            }
        ]
    }
]

app = Flask(__name__)


def create_store():
    request_data = request.get_json()  # Get the data from the request as a Dictionary
    new_store = {
        'name': request_data['name'],   # Store name
        'items': []
    }
    stores.append(new_store)
    return jsonify(new_store)


@app.route('/store/<string:name>', methods=['GET'])
def get_store(name):
    for store in stores:
        if store['Name'] == name:
            return jsonify(store)
    return jsonify({'message': 'store not found'})


@app.route('/store', methods=['GET'])
def get_stores():
    return jsonify({'stores': stores})  # gives back the list of dictionaries


@app.route('/store/<string>', methods=['POST'])
def create_item_in_store(name):
    request_data = request.get_json()
    for store in stores:
        if store['name'] == name:
            new_item = {
                'name': request_data['name'],
                'price': request_data['price']
            }
            store['items'].append(new_item)
            return jsonify(new_item)
    return jsonify({'message': 'store not found'})


@app.route('/store/<string:name>/item', methods=['GET'])
def get_items_in_store(name):
    for store in stores:
        if store['name'] == name:
            return jsonify({'items': store['items']})
    return jsonify({'message': 'store not found'})


app.run(port=5000)
