from flask import Flask, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)

# Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# Define the SQLAlchemy model
class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(200), nullable=True)
    quantity = db.Column(db.Integer, nullable=False)

    def to_dict(self):
            return {
                "id": self.id,
                "name": self.name,
                "description": self.description,
                "quantity": self.quantity
            }




# 1. Create a New Item (POST /items)
@app.route('/items', methods=['POST'])
def create_item():
    data = request.get_json()
    print("data", data)
    new_item = Item(
        name=data.get('name'),
        description=data.get('description'),
        quantity=data.get('quantity')
    )
    db.session.add(new_item)
    db.session.commit()
    result_data =  {
            "id": new_item.id,
            "name": new_item.name,
            "description": new_item.description,
            "quantity": new_item.quantity
            }
    return jsonify(result_data), 201


# 2. Retrieve All Items (GET /items)
@app.route('/items', methods=['GET'])
def get_items():
    items = Item.query.all()
    print("items", items)
    result = []
    for obj in items:
        result.append(obj.to_dict())
    return jsonify(result), 200
    # return jsonify([item.to_dict() for item in items]), 200

# 3. Retrieve a Single Item by ID (GET /items/<id>)
@app.route('/item/<int:id>', methods=['GET'])
def get_item(id):
    item = Item.query.get_or_404(id)
    # print("item", item, "type", type(item))
    return jsonify({"name": item.name, "id": item.id}), 200


# 4. Update an Item by ID (PUT /items/<id>)
@app.route('/items/<int:id>', methods=['PUT'])
def update_item(id):
    item = Item.query.get_or_404(id)
    data = request.get_json()
    item.name = data.get('name', item.name)
    item.description = data.get('description', item.description)
    item.quantity = data.get('quantity', item.quantity)
    db.session.commit()
    return jsonify(item.to_dict()), 200

# 5. Delete an Item by ID (DELETE /items/<id>)
@app.route('/items/<int:id>', methods=['DELETE'])
def delete_item(id):
    item = Item.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    return jsonify({"message": "Item deleted successfully"}), 200


# Create the database tables
with app.app_context():
    db.create_all()

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)