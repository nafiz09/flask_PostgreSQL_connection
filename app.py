from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Database connection configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:nafizml@localhost/demoDB'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Define the User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)

# Route to add a user via a POST request
@app.route('/add-user', methods=['POST'])
def add_user():
    # Get data from the request
    data = request.get_json()

    # Validate incoming data
    if 'name' not in data or 'email' not in data:
        return jsonify({"message": "Name and email are required"}), 400

    # Check if the email already exists
    existing_user = User.query.filter_by(email=data['email']).first()
    if existing_user:
        return jsonify({"message": "Email already exists"}), 400

    # Create a new user and add to the database
    new_user = User(name=data['name'], email=data['email'])
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User added successfully!"})

# Route to get all users (for demonstration)
@app.route('/get-users', methods=['GET'])
def get_users():
    users = User.query.all()
    user_list = [{"id": user.id, "name": user.name, "email": user.email} for user in users]
    return jsonify(user_list)

if __name__ == '__main__':
    app.run(debug=True)
