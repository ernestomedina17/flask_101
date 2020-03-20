#!/usr/local/bin/python3.7
from flask import Flask, jsonify  # jsonify in lower case because its a method

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
            return name
        else:
            return "Error, store not found"
    pass



@app.route('/store', methods=['GET'])
def get_stores():
    return jsonify({'stores': stores})  # gives back the list of dictionaries


@app.route('/store/<string>', methods=['POST'])
def create_item_in_store(name: str):
    pass


@app.route('/store/<string:name>/item', methods=['GET'])
def get_items_in_store(name):
    pass


app.run(port=5000)
