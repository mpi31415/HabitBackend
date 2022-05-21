from flask import Flask, jsonify, make_response, request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
import uuid
import jwt
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = '004f2af45d3a4e161a7dd2d17fdae47f'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///auth.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

from models import *

db.create_all()

from authentication import token_required

@app.route('/')
def index():
    return "hello"


@app.route('/register', methods=['POST'])
def signup_user():
    data = request.get_json()
    hashed_password = generate_password_hash(data['password'], method='sha256')

    new_user = Users(public_id=str(uuid.uuid4()), name=data['name'], password=hashed_password, admin=False)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'registered successfully'})


@app.route('/login', methods=['POST'])
def login_user():
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return make_response('could not verify', 401, {'Authentication': 'login required"'})

    user = Users.query.filter_by(name=auth.username).first()
    if check_password_hash(user.password, auth.password):
        token = jwt.encode(
            {'public_id': user.public_id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=45)},
            app.config['SECRET_KEY'], "HS256")

        return jsonify({'token': token})

    return make_response('could not verify2', 401, {'Authentication': '"login required"'})


@app.route('/users', methods=['GET'])
def get_all_users():
    users = Users.query.all()
    result = []
    for user in users:
        user_data = {}
        user_data['public_id'] = user.public_id
        user_data['name'] = user.name
        user_data['password'] = user.password
        user_data['admin'] = user.admin

        result.append(user_data)
    return jsonify({'users': result})


# @app.route('/book', methods=['POST'])
# @token_required
# def create_book(current_user):
#    data = request.get_json()
#
#    new_books = Books(name=data['name'], Author=data['Author'], Publisher=data['Publisher'],
#                      book_prize=data['book_prize'], user_id=current_user.id)
#    db.session.add(new_books)
#    db.session.commit()
#    return jsonify({'message': 'new books created'})


@app.route('/books', methods=['GET'])
@token_required
def get_progress(current_user):
    prog = Progress.query.filter_by(user_id=current_user.id).all()
    output = []
    for pro in prog:
        progress = {}
        progress['xp'] = pro.id
        progress['coins'] = pro.name
        progress['cards'] = pro.Author
        progress['win_loss_draw'] = pro.Publisher
        progress['goals'] = pro.book_prize
        output.append(progress)

    return jsonify({'progress': output})


# @app.route('/books/<book_id>', methods=['DELETE'])
# @token_required
# def delete_book(current_user, book_id):
#   book = Books.query.filter_by(id=book_id, user_id=current_user.id).first()
#  if not book:
#     return jsonify({'message': 'book does not exist'})

# db.session.delete(book)
# db.session.commit()
# return jsonify({'message': 'Book deleted'})


if __name__ == '__main__':
    app.run(debug=True)
