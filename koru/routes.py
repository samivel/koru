from flask import render_template, flash, redirect, url_for, request
from koru import app, db, bcrypt
from koru.forms import RegistrationForm, LoginForm, UpdateAccountForm, UpdatePhoto
from koru.models import User, Repertoire, Dancer
from flask_login import login_user, current_user, logout_user, login_required
import secrets
import os
from PIL import Image

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

# Function containing logic to save users new photo for the route below
def save_photo(form_photo):
    # Create random string to save photos name as
    random_hex = secrets.token_hex(8)
    # Split the file extention so that we can save the new image with the same extention
    _, f_ext = os.path.splitext(form_photo.filename)
    # Create new name for photo using the random hex, and keeping the extention
    photo_fn = random_hex + f_ext
    # Create path for new image. Start with the path to our koru directory, then joining the path within our directory, then joining the new photo name
    photo_path = os.path.join(app.root_path, 'static/images/profile_pics', photo_fn)
    
    # Resize image
    output_size = (250, 250)
    i = Image.open(form_photo)
    i.thumbnail(output_size)

    i.save(photo_path)
    return photo_fn

@app.route('/account-photo', methods=['GET', 'POST'])
@login_required
def account_photo():
    image_file = url_for('static', filename='images/profile_pics/' + current_user.image_file)
    form = UpdatePhoto()

    if form.validate_on_submit():
        new_photo = save_photo(form.photo.data)
        current_user.image_file = new_photo
        db.session.commit()

        flash('Photo Changed', 'success')
        return redirect(url_for('account_photo'))
    return render_template('account-photo.html', image_file=image_file, form=form)