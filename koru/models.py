from koru import db, login_manager
from flask_login import UserMixin

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
    

    def __repr__(self):
        return f"User('{self.first_name}' '{self.last_name}', '{self.email}', '{self.company_name}', '{self.image_file}')"

    

class Repertoire(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False)
    # The below 'dancers' is not a column in Repertoire. It is a query that is looking for the relationship to the 'Dancer' class
    dancers = db.relationship('Dancer', backref='repName', lazy=True)

    def __repr__(self):
        return f"Repertoire('{self.name}')"


class Dancer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    rank = db.Column(db.String(20), nullable=False)
    gender = db.Column(db.String(20), nullable=False)
    repertoire_id = db.Column(db.Integer, db.ForeignKey('repertoire.id'))
    

    def __repr__(self):
        return f"Dancer('{self.first_name}' '{self.last_name}', '{self.rank}', '{self.gender}')"