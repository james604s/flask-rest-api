from werkzeug.security import safe_str_cmp
from resources.user import User

def authenticate(username, password):
    user = User.find_by_username(username)
    print(user)
    if user and safe_str_cmp(user.password, password):
        return user
    # if user and user.password == password:
    #     return user

def identity(payload):
    print(payload)
    user_id = payload["identity"]
    return User.find_by_id(user_id)