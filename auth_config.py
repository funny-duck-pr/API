from werkzeug.security import generate_password_hash, check_password_hash

users_db = {
    'admin': {
        'password': 'pbkdf2:sha256:150000$V4n7Jbpl$eafebf78d1a91a835a8fe8a95db7d462c7bc55b7ed9d27ef43f5d00ef9c118f2',
        'role': 'Admin'
    },
    'user': {
        'password': 'pbkdf2:sha256:150000$Z8sY80lm$ae9d1f9d6345d5efb1289609c570e2fa9bcb69e4d0b990f47c5d1cc2eafcfa53',
        'role': 'User'
    }
}

from flask_httpauth import HTTPBasicAuth
auth = HTTPBasicAuth()

@auth.verify_password
def verify_password(username, password):
    user = users_db.get(username)
    if user and check_password_hash(user['password'], password):
        return username
    return None