from flask_restful import Resource, reqparse
from models.user import UserModel
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_refresh_token_required, get_jwt_identity, jwt_required
from models.user import UserModel

class UserRegister(Resource):
    parser = reqparse.RequestParser()  
    parser.add_argument('username',
                        type=str,
                        required=True,  
                        help="This field cannot be left blank!")
    parser.add_argument('password',
                        type=str,
                        required=True,  
                        help="This field cannot be left blank!")

    def post(self):
        data = self.parser.parse_args()
        if UserModel.find_by_username(data['username']): 
            return {"message": "A user with that username already exists"}, 400

        user = UserModel(**data)    # Unpack data Dictionary
        # user = UserModel(data['username'], data['password'])
        user.save_to_db()
        
        return {"message": "User created successfully."}, 201


class UserLogin(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!")
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!")

    def post(self):
        data = self.parser.parse_args()
        user = UserModel.find_by_username(data['username']):
            return {"message": "A user with that username already exists"}, 400

        if user and safe_str_cmp(user.password, data['password']):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)
            return {
                'access_token': access_token,
                'refresh_token': refresh_token
            }, 200

        return {'message': 'Invalid credentials'}, 401


# Blacklist the token so they need to login back again
class UserLogout(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti'] # jti is "JWT ID", a unique id for JWT
        BLACKLIST.add(jti)
        return {'message': 'Successfully logged out.'}, 200




class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        # The generated token will not be fresh
        new_token = create_access_token(identity=current_user, fresh=False)
        return {'access_token': new_token}, 200


