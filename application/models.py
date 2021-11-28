from .database import db
from flask_security import UserMixin, RoleMixin

roles_users = db.Table(
    'roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
)
class User(db.Model, UserMixin):
    __tablename_ = 'user'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String)
    email = db.Column(db.String, unique = True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    roles = db.relationship('Role', secondary=roles_users, backref=db.backref('users', lazy='dynamic'))

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String)
    
class Decks(db.Model):
    __tablename__ = 'decks'
    deck_id = db.Column(db.Integer, primary_key=True)
    deck_name = db.Column(db.String(50))
    deck_description = db.Column(db.String)
    access_time = db.Column(db.DateTime)
    id = db.Column(db.Integer, db.ForeignKey('user.uid'), nullable=False)

class Cards(db.Model):
    __tablename__ = 'cards'
    card_id = db.Column(db.Integer, primary_key=True)
    card_name = db.Column(db.String(50))
    front = db.Column(db.String(50))
    back = db.Column(db.String(50))
    score = db.Column(db.Integer)
    deck_id = db.Column(db.Integer, db.ForeignKey('decks.deck_id'), nullable=False)