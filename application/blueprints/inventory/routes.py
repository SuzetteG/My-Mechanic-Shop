
# Inventory routes placeholder
from . import inventory_bp

# DELETE route for inventory item by id
@inventory_bp.route('/<int:item_id>', methods=['DELETE'])
def delete_inventory_item(item_id):
    item = Inventory.query.get(item_id)
    if not item:
        return jsonify({'error': 'Item not found'}), 404
    db.session.delete(item)
    db.session.commit()
    return jsonify({'message': f'Inventory item {item_id} deleted'}), 200

@inventory_bp.route('/')
def inventory_home():
    # List all inventory items
    items = Inventory.query.all()
    result = [
        {
            'id': item.id,
            'name': item.name,
            'quantity': item.quantity,
            'price': float(item.price) if item.price is not None else None
        }
        for item in items
    ]
    return jsonify(result)


# Sample PUT route to update an inventory item by item_id
from flask import request, jsonify
from application.blueprints.models import Inventory
from application.extensions import db

@inventory_bp.route('/<int:item_id>', methods=['PUT'])
def update_inventory_item(item_id):
    item = Inventory.query.get(item_id)
    if not item:
        return jsonify({'error': 'Item not found'}), 404
    data = request.get_json()
    # Example: update name and quantity fields
    if 'name' in data:
        item.name = data['name']
    if 'quantity' in data:
        item.quantity = data['quantity']
    if 'price' in data:
        item.price = data['price']
    db.session.commit()
    return jsonify({'message': f'Updated item {item_id}', 'item': {'id': item.id, 'name': item.name, 'quantity': item.quantity, 'price': float(item.price) if item.price is not None else None}})


# GET route to show quantity and price of a specific part
@inventory_bp.route('/<int:item_id>', methods=['GET'])
def get_inventory_item(item_id):
    item = Inventory.query.get(item_id)
    if not item:
        return jsonify({'error': 'Item not found'}), 404
    return jsonify({'id': item.id, 'name': item.name, 'quantity': item.quantity, 'price': float(item.price) if item.price is not None else None})


# POST route to create a new inventory item
@inventory_bp.route('/', methods=['POST'])
def create_inventory_item():
    data = request.get_json()
    name = data.get('name')
    quantity = data.get('quantity')
    if not name or quantity is None:
        return jsonify({'error': 'Name and quantity are required'}), 400
    item = Inventory(name=name, quantity=quantity)
    db.session.add(item)
    db.session.commit()
    return jsonify({'message': 'Inventory item created', 'item': {'id': item.id, 'name': item.name, 'quantity': item.quantity}}), 201
