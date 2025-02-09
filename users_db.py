from werkzeug.security import generate_password_hash

users_db = {
    'admin': {'password': generate_password_hash('adminpass'), 'role': 'Admin'},
    'user': {'password': generate_password_hash('userpass'), 'role': 'User'}
}