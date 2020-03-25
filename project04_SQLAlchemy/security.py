from werkzeug.security import safe_str_cmp
from models.user import UserModel

# JWT Authentication method
def authenticate(username, password):
    user = UserModel.find_by_username(username)
    # safe string comparison
    if user and safe_str_cmp(user.password, password):  
        return user

# JWT Identification method, the parameter represents the request body in the form of a JWT encoded Token, E.g.
# {'exp': 1585088122, 'iat': 1585087822, 'nbf': 1585087822, 'identity': 4}
def identity(payload):
    user_id = payload['identity']
    # Returns the user id, username and password to the App
    return UserModel.find_by_id(user_id)
