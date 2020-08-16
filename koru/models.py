from koru import db, login_manager
from flask_login import UserMixin
from flask import current_app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    company_name = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(60), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.png')
    password = db.Column(db.String(60), nullable=False)
    dancers = db.relationship('Dancer', backref='company', lazy=True)
    balletmasters= db.relationship('BalletMaster', backref='company', lazy=True)
    accompanists = db.relationship('Accompanist', backref='company', lazy=True)
    repetiteurs = db.relationship('Repetiteur', backref='company', lazy=True)


    # Make reset token for resetting password
    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    # Verifies the token to reset password
    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY']) 
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.first_name}' '{self.last_name}', '{self.email}', '{self.company_name}', '{self.image_file}')"


    

class Dancer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    rank = db.Column(db.String(20), nullable=False)
    gender = db.Column(db.String(20), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    

    def __repr__(self):
        return f"Dancer('{self.first_name}' '{self.last_name}', '{self.rank}', '{self.gender}')"

    


class BalletMaster(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    gender = db.Column(db.String(20), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    

    def __repr__(self):
        return f"Ballet Master('{self.first_name}' '{self.last_name}', '{self.gender}')"


class Accompanist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    gender = db.Column(db.String(20), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    

    def __repr__(self):
        return f"Accompanist('{self.first_name}' '{self.last_name}', '{self.gender}')"


class Repetiteur(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    gender = db.Column(db.String(20), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    

    def __repr__(self):
        return f"Repetiteur('{self.first_name}' '{self.last_name}', '{self.gender}')"
















class Repertoire(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False)
    
    

    def __repr__(self):
        return f"Repertoire('{self.name}')"

