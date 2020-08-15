
from flask import render_template, flash, redirect, url_for, request, Blueprint
from koru import db, bcrypt
from koru.users.forms import RegistrationForm, LoginForm, UpdateAccountForm, UpdatePhoto, ResetPasswordForm, RequestResetForm
from koru.models import User
from flask_login import login_user, current_user, logout_user, login_required
from koru.users.helpers import save_photo, send_reset_email



users = Blueprint('users', __name__)


@users.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
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
        login_user(user)
        # Flash success message and redirect to login
        flash(f'Account created for {form.first_name.data} {form.last_name.data}, with {form.company_name.data}!', 'success')
        return redirect(url_for('users.login'))

    return render_template('register.html', form=form)



@users.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

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
            return redirect(next_page) if next_page else redirect(url_for('main.index'))
            
        else:
            flash('Login Unsuccessful', 'danger')
    return render_template('login.html', form=form)


@users.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    # Send user home if logged in
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RequestResetForm()
    # Gets users info based on email and sends a reset link
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('Check your email for reset link', 'info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', title='Reset Password', form=form)


@users.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
        # Verifies if token is valid
    user = User.verify_reset_token(token)
    if not user:
        flash('That is an invalid or expired reset link', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    # Updates users password and logs in
    if form.validate_on_submit():
        # Hash users password
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        login_user(user)
        flash('Password Updated', 'success')
        return redirect(url_for('main.index'))
    

    return render_template('reset_token.html', title='Reset Password', form=form)


@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@users.route('/account', methods=['GET', 'POST'])
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
        return redirect(url_for('users.account'))
    
    # If request method is get, fill table with current user data
    elif request.method == 'GET':
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
        form.company_name.data = current_user.company_name
        form.email.data = current_user.email
    return render_template('account.html', form=form, title='Account')



@users.route('/account-photo', methods=['GET', 'POST'])
@login_required
def account_photo():
    # create full path to users current photo
    image_file = url_for('static', filename='images/profile_pics/' + current_user.image_file)
    form = UpdatePhoto()

    if form.validate_on_submit():
        # Use save_photo from helpers
        new_photo = save_photo(form.photo.data, str(current_user.id))
        # Update users photo and commit
        current_user.image_file = new_photo
        db.session.commit()

        flash('Profile pic updated', 'success')
        return redirect(url_for('users.account_photo'))
    return render_template('account-photo.html', image_file=image_file, form=form, title='Account photo')

