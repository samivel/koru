from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager



app = Flask(__name__)
# Configure secret key and Database uri
app.config['SECRET_KEY'] = '1b13c35d94c96ea3dffe982f0000d7d4'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///koru.db'

# Initialize database instance
db = SQLAlchemy(app)

bcrypt = Bcrypt(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = "warning"
from koru import routes