from password import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    website_passwords = db.relationship('Password', backref='owner', lazy=True)

    def __repr__(self):
        return f'User("{self.email}")'


class Password(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    website = db.Column(db.String(120), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=True)
    username = db.Column(db.String(60), nullable=True)
    password = db.Column(db.String(60), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f'Password("{self.website}","{self.username}", "{self.email}")'