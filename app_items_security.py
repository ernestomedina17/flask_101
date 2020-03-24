from werkzeug.security import safe_str_cmp
from app_items_user import User

users = [
    User(1, 'bob', 'asdf')
]

# for each user, get username
username_mapping = {u.username: u for u in users}   
# for each user, get id
userid_mapping = {u.id: u for u in users}           


def authenticate(username, password):
    # if no matching Key, then None
    user = username_mapping.get(username, None)  
    # safe string comparison
    if user and safe_str_cmp(user.password, password):  
        return user


def identity(payload):
    user_id = payload['identity']
    return userid_mapping.get(user_id, None)
