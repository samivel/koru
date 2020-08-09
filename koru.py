from flask import Flask, render_template, flash, redirect, url_for
from forms import RegistrationForm, LoginForm


app = Flask(__name__)

app.config['SECRET_KEY'] = '1b13c35d94c96ea3dffe982f0000d7d4'



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