from flask import Flask, render_template, flash, redirect, url_for
from forms import RegistrationForm, LoginForm
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

# Configure secret key and Database uri
app.config['SECRET_KEY'] = '1b13c35d94c96ea3dffe982f0000d7d4'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///koru.db'

# Initialize database instance
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    company_name = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(60), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
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

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account Created for {form.first_name.data}, {form.company_name.data}!', 'success')
        return redirect(url_for('index'))

    return render_template('register.html', form=form)



@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'samivel@gmail.com' and form.password.data == 'eeeedddd':
            flash('Login Successful', 'success')
            return redirect(url_for('index'))
        else:
            flash('NO WAY', 'danger')
    return render_template('login.html', form=form)






if __name__ == '__main__':
    app.run(debug=True)