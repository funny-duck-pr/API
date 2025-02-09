from flask import request, jsonify
from werkzeug.security import check_password_hash
from users_db import users_db

def check_auth(username, password):

    user = users_db.get(username)
    if user and check_password_hash(user['password'], password):
        return user
    return None

def role_required(role):
    def decorator(func):
        def wrapper(*args, **kwargs):
            auth = request.authorization
            if not auth or not check_auth(auth.username, auth.password):
                return jsonify({'message': 'Authentication required'}), 401

            user = users_db.get(auth.username)
            if user['role'] != role:
                return jsonify({'message': 'Permission denied'}), 403

            return func(*args, **kwargs)
        return wrapper
    return decorator