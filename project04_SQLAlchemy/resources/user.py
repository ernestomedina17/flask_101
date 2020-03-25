import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel

class UserRegister(Resource):
    # Get request in order to validate it
    parser = reqparse.RequestParser()  
    # 'username' is required in the request
    parser.add_argument('username',
                        type=str,
                        required=True,  
                        help="This field cannot be left blank!")
    # 'password' is required in the request
    parser.add_argument('password',
                        type=str,
                        required=True,  
                        help="This field cannot be left blank!")

    def post(self):
        data = self.parser.parse_args()
        # means its not None and it exists already, return HTTP Status Code 400 (Bad request)
        if UserModel.find_by_username(data['username']): 
            return {"message": "A user with that username already exists"}, 400

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "INSERT INTO users VALUES (NULL, ?, ?)"

        cursor.execute(query, (data['username'], data['password']))
        connection.commit()
        connection.close()
        return {"message": "User created successfully."}, 201
