from main import db

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.Integer)
    name = db.Column(db.String(50))
    password = db.Column(db.String(50))
    admin = db.Column(db.Boolean)


class Progress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    xp = db.Column(db.String(50), unique=True, nullable=False)
    coins = db.Column(db.String(50), unique=True, nullable=False)
    cards = db.Column(db.String(50), nullable=False)
    win_loss_draw = db.Column(db.String(50))
    goals = db.Column(db.Integer)

class Goals(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    description = db.Column(db.String(50), unique=True, nullable=False)
    duration = db.Column(db.Integer, unique=True, nullable=False)
