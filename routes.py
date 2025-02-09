from flask import Blueprint, jsonify, request
from werkzeug.security import check_password_hash
from app import users_db, auth

items_bp = Blueprint('items', __name__)

items = []

@auth.verify_password
def verify_password(username, password):
    user = users_db.get(username)
    if user and check_password_hash(user['password'], password):
        return username
    return None

def role_required(role):
    def decorator(func):
        def wrapper(*args, **kwargs):
            auth = request.authorization
            if not auth or not verify_password(auth.username, auth.password):
                return jsonify({'message': 'Authentication required'}), 401

            user = users_db.get(auth.username)
            if user['role'] != role:
                return jsonify({'message': 'Permission denied'}), 403

            return func(*args, **kwargs)
        return wrapper
    return decorator

@items_bp.route('/api/items', methods=['GET'])
def get_items():
    return jsonify(items), 200

@items_bp.route('/api/items', methods=['POST'])
@auth.login_required
@role_required('Admin')
def create_item():
    item_data = request.get_json()
    item = {
        'id': len(items) + 1,
        'name': item_data['name'],
        'description': item_data.get('description', '')
    }
    items.append(item)
    return jsonify(item), 201

@items_bp.route('/api/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    item = next((item for item in items if item['id'] == item_id), None)
    if item is None:
        return jsonify({'message': 'Item not found'}), 404
    return jsonify(item), 200

@items_bp.route('/api/items/<int:item_id>', methods=['PATCH'])
@auth.login_required
@role_required('Admin')
def update_item(item_id):
    item = next((item for item in items if item['id'] == item_id), None)
    if item is None:
        return jsonify({'message': 'Item not found'}), 404

    item_data = request.get_json()
    item['name'] = item_data.get('name', item['name'])
    item['description'] = item_data.get('description', item['description'])

    return jsonify(item), 200

@items_bp.route('/api/items/<int:item_id>', methods=['DELETE'])
@auth.login_required
@role_required('Admin')
def delete_item(item_id):
    item = next((item for item in items if item['id'] == item_id), None)
    if item is None:
        return jsonify({'message': 'Item not found'}), 404

    items.remove(item)
    return jsonify({'message': 'Item deleted'}), 200