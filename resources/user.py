import sqlite3
from flask_restful import Resource, reqparse


class User:
    def __init__(self, _id, username, password):
        self.id = _id
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(cls, username):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "SELECT * FROM users WHERE username=?"
        # Tuple, with single item requires a comma
        result = cursor.execute(query, (username,))  
        row = result.fetchone()
        if row:
            user = cls(*row)
            # user = cls(row[0], row[1], row[2])  # long version of above
        else:
            user = None

        connection.close()
        return user

    @classmethod
    def find_by_id(cls, _id):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "SELECT * FROM users WHERE id=?"
        # Tuple, with single item requires a comma
        result = cursor.execute(query, (_id,))  
        row = result.fetchone()
        if row:
            user = cls(*row)
            # user = cls(row[0], row[1], row[2])  # long version of above
        else:
            user = None

        connection.close()
        return user


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
        if User.find_by_username(data['username']): 
            return {"message": "A user with that username already exists"}, 400

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "INSERT INTO users VALUES (NULL, ?, ?)"

        cursor.execute(query, (data['username'], data['password']))
        connection.commit()
        connection.close()
        return {"message": "User created successfully."}, 201
