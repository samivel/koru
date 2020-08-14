from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
import os


app = Flask(__name__)
# Configure secret key and Database uri
app.config['SECRET_KEY'] = '1b13c35d94c96ea3dffe982f0000d7d4'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///koru.db'


# Initialize database instance
db = SQLAlchemy(app)

bcrypt = Bcrypt(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = "info"
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'korukorukorudance'
app.config['MAIL_PASSWORD'] = 'korukoru'
mail = Mail(app)

from koru import routes