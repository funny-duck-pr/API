from flask import Flask
app = Flask(__name__)

from routes import items_bp
app.register_blueprint(items_bp)

if __name__ == '__main__':
    app.run(debug=True)