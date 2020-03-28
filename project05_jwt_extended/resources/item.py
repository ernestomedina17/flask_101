from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_claims, jwt_optional, get_jwt_identity. fresh_jwt_requited
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

    #@jwt_required()
    @jwt_required
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'Item not found'}, 404

    @fresh_jwt_requited
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
        
    @jwt_required
    def delete(self, name):
        claims = get_jwt_claims()
        if not claims['is_admin']:
            return {'message': 'Admin privilege required'}, 401

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
    @jwt_optional
    def get(self):
        # who the user is
        user_id = get_jwt_identity()
        items = [x.json() for x in ItemModel.find_all()]
        if user_id:
            return {'items': items}, 200
        return {'items': [item.['name'] for item in items],
                'message': 'Mora data available if you log in.'
        }, 200


