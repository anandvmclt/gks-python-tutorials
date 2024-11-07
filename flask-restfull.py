from flask import Flask, request
from flask_restful import Resource, Api, abort
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)

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

# Create the database tables
with app.app_context():
    db.create_all()

### Step 4: Define Flask-RESTful Resources

class ItemListResource(Resource):
    # Get all items
    def get(self):
        type_ = request.args.get('type') 
        print("Query param type :", type_)
        if type_ is None:
            items = Item.query.all()
            return [item.to_dict() for item in items], 200
        else:
            items = Item.query.filter_by(name=type_).all()
        return [item.to_dict() for item in items], 200

    # Create a new item
    def post(self):
        data = request.get_json()
        new_item = Item(
            name=data.get('name'),
            description=data.get('description'),
            quantity=data.get('quantity')
        )
        db.session.add(new_item)
        db.session.commit()
        return new_item.to_dict(), 201


class ItemResource(Resource):
    # Get a single item by ID
    def get(self, item_id):
        item = Item.query.get_or_404(item_id)
        return item.to_dict(), 200

    # Update an item by ID
    def put(self, item_id):
        item = Item.query.get_or_404(item_id)
        data = request.get_json()
        item.name = data.get('name', item.name)
        item.description = data.get('description', item.description)
        item.quantity = data.get('quantity', item.quantity)
        db.session.commit()
        return item.to_dict(), 200

    # Delete an item by ID
    def delete(self, item_id):
        item = Item.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()
        return {"message": "Item deleted successfully"}, 200


### Step 5: Add Resources to the API

api.add_resource(ItemListResource, '/items')        # For listing and creating items
api.add_resource(ItemResource, '/items/<int:item_id>')  # For CRUD operations on single items

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
