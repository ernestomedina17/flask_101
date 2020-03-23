from werkzeug.security import safe_str_cmp
from user2 import User

users = [
    User(1, 'bob', 'asdf')
]


username_mapping = {u.username: u for u in users}   # for each user, get username
userid_mapping = {u.id: u for u in users}           # for each user, get id


def authenticate(username, password):
    user = username_mapping.get(username, None)  # if no matching Key, then None
    if user and safe_str_cmp(user.password, password):  # string comparison
        return user


def identity(payload):
    user_id = payload['identity']   # ?
    return userid_mapping.get(user_id, None)
