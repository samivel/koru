
from flask import render_template, redirect, url_for, Blueprint

from koru.models import Dancer, BalletMaster, Repetiteur, Accompanist
from flask_login import current_user




main = Blueprint('main', __name__)


@main.route('/landing')
def landing():
    return render_template('landing.html')


@main.route('/')
def index():
    if current_user.is_authenticated == False:
        return redirect(url_for('main.landing'))
    # This line queries the database for all dancers belonging to the current user, and orders them by last name
    dancers = Dancer.query.filter_by(user_id=current_user.id).order_by(Dancer.last_name).all()
    bms = BalletMaster.query.filter_by(user_id=current_user.id).order_by(BalletMaster.last_name).all()
    accompanists = Accompanist.query.filter_by(user_id=current_user.id).order_by(Accompanist.last_name).all()
    repetiteurs = Repetiteur.query.filter_by(user_id=current_user.id).order_by(Repetiteur.last_name).all()
    return render_template('index.html', title='Home', dancers=dancers, bms=bms, accompanists=accompanists, repetiteurs=repetiteurs)
