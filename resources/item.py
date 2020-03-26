from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

class Item(Resource):
    parser = reqparse.RequestParser() 
    parser.add_argument('price',
                        type=float,
                        required=True,  
                        help="This field cannot be left blank!")

    parser.add_argument('store_id',
                        type=int,
                        required=True,  
                        help="Every item needs a store id")

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'Item not found'}, 404

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': "An item with name '{}' already exists".format(name)}, 400
        data = self.parser.parse_args()
        item = ItemModel(name, **data)
        # item = ItemModel(name, data['price'], data['store_id'])
        try:
            item.save_to_db()
        except:
            return {'message': "An error happended while trying to insert a new item"}
        return item.json(), 201  # 201 (Created)
        
    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
        return {'message': 'Item deleted'}

    def put(self, name):
        data = self.parser.parse_args()
        item = ItemModel.find_by_name(name)
        
        if item is None:
            item = ItemModel(name, **data)
            # item = ItemModel(name, data['price'], data['store_id'])
        else:
            item.price = data['price']
            
        item.save_to_db()        
        return item.json()
            
        
class ItemList(Resource):
    def get(self):
        # List comprehension, for each row in the table, convert it to json or dic
        return {'items': [item.json() for item in ItemModel.query.all()]}
        # OR with lambda, map and map reduce will resemble JavaScript 
        # return {'items': list(map(lambda x: x.json, ItemModel.query.all()))}
