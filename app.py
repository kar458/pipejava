from flask import Flask, jsonify, request

app = Flask(__name__)

# In-memory data storage (as an example)
data = [
    {"id": 1, "name": "Item 1", "description": "This is item 1"},
    {"id": 2, "name": "Item 2", "description": "This is item 2"}
]

# Get all items
@app.route('/items', methods=['GET'])
def get_items():
    return jsonify(data), 200

# Get a single item by ID
@app.route('/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    item = next((item for item in data if item["id"] == item_id), None)
    if item:
        return jsonify(item), 200
    return jsonify({"error": "Item not found"}), 404

# Create a new item
@app.route('/items', methods=['POST'])
def create_item():
    new_item = request.json
    if not new_item or not new_item.get('name'):
        return jsonify({"error": "Invalid input"}), 400
    
    new_item["id"] = data[-1]["id"] + 1 if data else 1
    data.append(new_item)
    return jsonify(new_item), 201

# Update an existing item (full update)
@app.route('/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    item = next((item for item in data if item["id"] == item_id), None)
    if not item:
        return jsonify({"error": "Item not found"}), 404
    
    updated_item = request.json
    if not updated_item or not updated_item.get('name'):
        return jsonify({"error": "Invalid input"}), 400
    
    item.update(updated_item)
    return jsonify(item), 200

# Partial update an existing item
@app.route('/items/<int:item_id>', methods=['PATCH'])
def partial_update_item(item_id):
    item = next((item for item in data if item["id"] == item_id), None)
    if not item:
        return jsonify({"error": "Item not found"}), 404
    
    updates = request.json
    item.update(updates)
    return jsonify(item), 200

# Delete an item
@app.route('/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    global data
    data = [item for item in data if item["id"] != item_id]
    return jsonify({"message": f"Item {item_id} deleted"}), 200

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
