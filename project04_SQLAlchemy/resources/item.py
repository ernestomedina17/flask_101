import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel


class Item(Resource):
    # Gets the Request so you can parse it for validation
    parser = reqparse.RequestParser() 
    # The 'price' argument is required in the request
    parser.add_argument('price',
                        type=float,
                        required=True,  
                        help="This field cannot be left blank!")

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
        item = ItemModel(name, data['price'])
        
        try:
            item.insert()
        except:
            # Internal Server Error
            return {"message": "An error ocurred while inserting the item."}, 500 
        
        # 201 (Created)
        return item.json(), 201  
        
    def delete(self, name):
        if ItemModel.find_by_name(name):
            connection = sqlite3.connect('data.db')
            cursor = connection.cursor()
            query = "DELETE FROM items WHERE name=?"
            cursor.execute(query, (name,))
            connection.commit()
            connection.close()
            return {'message': "Item('{}') deleted".format(name)}
        # Precondition Failed    
        return {"message": "Item not found"}, 412

    def put(self, name):
        data = self.parser.parse_args()
        item = ItemModel.find_by_name(name)
        updated_item = ItemModel(name, data['price'])
        
        if item is None:
            try:
                updated_item.insert()
            except:
                return {"message": "An error ocurred while trying to insert a new item"}
        else:
            try:
                updated_item.update()
            except:
                return {"message": "An error ocurred while trying to update a new item"}
        return updated_item.json()
            
        
class ItemList(Resource):
    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "SELECT * FROM items"
        result = cursor.execute(query)
        items = []
        for row in result:
            items.append({'name': row[0], 'price': row[1]})
            
        connection.commit()
        connection.close()
        
        return {'items': items}
