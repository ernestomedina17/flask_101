#!/usr/local/bin/python3.7
from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)



@app.route('/')
def home():
    return render_template('index.html')


@app.route('/store', methods=['POST'])
def create_store():
    request_data = request.get_json()  # Get the data from the request as a Dictionary
    new_store = {
        'name': request_data['name'],  # Store name
        'items': []
    }
    stores.append(new_store)
    return jsonify(new_store)




app.run(port=5000)
