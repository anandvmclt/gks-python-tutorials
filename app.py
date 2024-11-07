from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy

from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
api = Api(app)

# Configure the SQLite database and JWT
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'super-secret'  # Change this to a strong secret key in production
db = SQLAlchemy(app)
jwt = JWTManager(app)

# User model for authentication
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)

    def to_dict(self):
        return {"id": self.id, "username": self.username}

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    

# Item model (same as before, with CRUD)
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


### Authentication Resources
class RegisterResource(Resource):
    def post(self):
        data = request.get_json()
        if User.query.filter_by(username=data['username']).first():
            return {"message": "User already exists"}, 400

        new_user = User(username=data['username'])
        new_user.set_password(data['password'])
        db.session.add(new_user)
        db.session.commit()
        return {"message": "User created successfully"}, 201


class LoginResource(Resource):
    def post(self):
        data = request.get_json()
        user = User.query.filter_by(username=data['username']).first()
        if user and user.check_password(data['password']):
            # access_token = create_access_token(identity=user.id)
            access_token = create_access_token(
                identity={"id": user.id, "username": user.username},
                additional_claims={"user_info": {"username": user.username}}  # Add custom claims
            )
           
            return {"access_token": access_token, "id": user.id, "username": user.username}, 200
        return {"message": "Invalid credentials"}, 401

### CRUD Resources with JWT Protection
class ItemListResource(Resource):
    # @jwt_required()
    def get(self):
        items = Item.query.all()
        return [item.to_dict() for item in items], 200

    @jwt_required()
    def post(self):
        data = request.get_json()
        new_item = Item(
            name=data['name'],
            description=data.get('description'),
            quantity=data['quantity']
        )
        db.session.add(new_item)
        db.session.commit()
        return new_item.to_dict(), 201


class ItemResource(Resource):
    @jwt_required()
    def get(self, item_id):
        user_id = get_jwt_identity()
        username = User.query.get(user_id).username
        print("User ID:", user_id, username)
        # Udate user or item and commit the DB session
        item = Item.query.get_or_404(item_id)
        return item.to_dict(), 200

    @jwt_required()
    def put(self, item_id):
        item = Item.query.get_or_404(item_id)
        data = request.get_json()
        item.name = data.get('name', item.name)
        item.description = data.get('description', item.description)
        item.quantity = data.get('quantity', item.quantity)
        db.session.commit()
        return item.to_dict(), 200

    @jwt_required()
    def delete(self, item_id):
        item = Item.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()
        return {"message": "Item deleted successfully"}, 200



# Create the database tables
with app.app_context():
    db.create_all()

api.add_resource(RegisterResource, '/register')         # User registration
api.add_resource(LoginResource, '/login')   
api.add_resource(ItemListResource, '/items')            # Protected list and create items
api.add_resource(ItemResource, '/items/<int:item_id>')  # Protected single item CRUD

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)