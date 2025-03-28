from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:nafizml@localhost/demoDB'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)

@app.route('/add-user', methods=['GET'])
def add_user():
    new_user = User(name="John Doe", email="johndoe@example.com")
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User added successfully!"})

if __name__ == '__main__':
    app.run(debug=True)
