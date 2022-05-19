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


def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None
        if 'x-access-tokens' in request.headers:
            token = request.headers['x-access-tokens']

        if not token:
            return jsonify({'message': 'a valid token is missing'})
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = Users.query.filter_by(public_id=data['public_id']).first()
        except:
            return jsonify({'message': 'token is invalid'})

        return f(current_user, *args, **kwargs)

    return decorator




#@app.route('/book', methods=['POST'])
#@token_required
#def create_book(current_user):
#    data = request.get_json()
#
#    new_books = Books(name=data['name'], Author=data['Author'], Publisher=data['Publisher'],
#                      book_prize=data['book_prize'], user_id=current_user.id)
#    db.session.add(new_books)
#    db.session.commit()
#    return jsonify({'message': 'new books created'})



#@app.route('/books/<book_id>', methods=['DELETE'])
#@token_required
#def delete_book(current_user, book_id):
 #   book = Books.query.filter_by(id=book_id, user_id=current_user.id).first()
  #  if not book:
   #     return jsonify({'message': 'book does not exist'})

    #db.session.delete(book)
    #db.session.commit()
    #return jsonify({'message': 'Book deleted'})


if __name__ == '__main__':
    app.run(debug=True)
