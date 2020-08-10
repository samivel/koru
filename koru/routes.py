from flask import render_template, flash, redirect, url_for
from koru import app, db, bcrypt
from koru.forms import RegistrationForm, LoginForm
from koru.models import User, Repertoire, Dancer
from flask_login import login_user, current_user, logout_user, login_required




@app.route('/')
def index():
    
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    # Get info from form
    form = RegistrationForm()
    # If form is validated:
    if form.validate_on_submit():
        # Hash users password
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        # Create user class from form info
        user = User(first_name=form.first_name.data, last_name=form.last_name.data, company_name=form.company_name.data, email=form.email.data.lower(), password=hashed_password)
        # Add user object to db and commit
        db.session.add(user)
        db.session.commit()
        # Flash success message and redirect to login
        flash(f'Account created for {form.first_name.data} {form.last_name.data}, with {form.company_name.data}!', 'success')
        return redirect(url_for('login'))

    return render_template('register.html', form=form)



@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    # Get data from login form
    if form.validate_on_submit():
        # Query database for user
        user = User.query.filter_by(email=form.email.data.lower()).first()

        # If credentials match, log user in
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash('Login Successful', 'success')
            return redirect(url_for('index'))
        else:
            flash('Login Unsuccessful', 'danger')
    return render_template('login.html', form=form)



@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/account')
@login_required
def account():
    return render_template('account.html')