
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

# JSON is a Python's Dictionary text/string 
from flask import Flask, jsonify   # lower case because is a method
app = Flask(__name__)	
@app.route('/store', methods=['POST'])
def create_store():
    pass
@app.route('/store/<string:name>', methods=['GET'])
def get_store(name):
    pass 
@app.route('/store', methods=['GET'])
def get_stores():
    return jsonify({'stores': stores}) # gives back the list of dictionaries
@app.route('/store/<string>', methods=['POST'])
def create_item_in_store(name: str):
    pass 
@app.route('/store/<string:name>/item', methods=['GET'])
def get_items_in_store(name):
    pass 

app.run(port=5000) 
