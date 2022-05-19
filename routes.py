from main import *

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


@app.route('/get/progress', methods=['GET'])
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

