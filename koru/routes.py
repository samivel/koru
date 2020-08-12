from flask import render_template, flash, redirect, url_for, request, session
from koru import app, db, bcrypt
from koru.forms import RegistrationForm, LoginForm, UpdateAccountForm, UpdatePhoto
from koru.models import User, Repertoire, Dancer
from flask_login import login_user, current_user, logout_user, login_required
from koru.helpers import save_photo

@app.route('/landing')
def landing():
    return render_template('landing.html')


@app.route('/')
def index():
    if current_user.is_authenticated == False:
        return redirect(url_for('landing'))
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
            

            # Get the GET params to see if user landed on login page trying to access a 'login required' page, so that we can send them there after login.
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index'))
            
        else:
            flash('Login Unsuccessful', 'danger')
    return render_template('login.html', form=form)



@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    
    form = UpdateAccountForm()
    
    # If form is valid, update the user db table with the provided data
    if form.validate_on_submit():
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.company_name = form.company_name.data
        current_user.email = form.email.data.lower()
        db.session.commit()
        flash('Account Updated', 'success')
        return redirect(url_for('account'))
    
    # If request method is get, fill table with current user data
    elif request.method == 'GET':
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
        form.company_name.data = current_user.company_name
        form.email.data = current_user.email
    return render_template('account.html', form=form,)



@app.route('/account-photo', methods=['GET', 'POST'])
@login_required
def account_photo():
    # create full path to users current photo
    image_file = url_for('static', filename='images/profile_pics/' + current_user.image_file)
    form = UpdatePhoto()

    if form.validate_on_submit():
        # Use save_photo from helpers
        new_photo = save_photo(form.photo.data)
        # Update users photo and commit
        current_user.image_file = new_photo
        db.session.commit()

        flash('Profile pic updated', 'success')
        return redirect(url_for('account_photo'))
    return render_template('account-photo.html', image_file=image_file, form=form)