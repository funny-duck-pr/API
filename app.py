from flask import Flask, jsonify, request

app = Flask(__name__)

items = []

@app.route('/api/items', methods=['GET'])
def get_items():
    return jsonify(items), 200

@app.route('/api/items', methods=['POST'])
def create_item():
    item_data = request.get_json()
    item = {
        'id': len(items) + 1,
        'name': item_data['name'],
        'description': item_data.get('description', '')
    }
    items.append(item)
    return jsonify(item), 201

@app.route('/api/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    item = next((item for item in items if item['id'] == item_id), None)
    if item is None:
        return jsonify({'message': 'Item not found'}), 404
    return jsonify(item), 200

@app.route('/api/items/<int:item_id>', methods=['PATCH'])
def update_item(item_id):
    item = next((item for item in items if item['id'] == item_id), None)
    if item is None:
        return jsonify({'message': 'Item not found'}), 404

    item_data = request.get_json()
    item['name'] = item_data.get('name', item['name'])
    item['description'] = item_data.get('description', item['description'])

    return jsonify(item), 200

@app.route('/api/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    item = next((item for item in items if item['id'] == item_id), None)
    if item is None:
        return jsonify({'message': 'Item not found'}), 404

    items.remove(item)
    return jsonify({'message': 'Item deleted'}), 200

if __name__ == '__main__':
    app.run(debug=True)