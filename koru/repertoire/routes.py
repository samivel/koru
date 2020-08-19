from flask import render_template, flash, redirect, url_for, request, abort, Blueprint
from koru import db
from koru.repertoire.forms import AddRepertoireForm
from koru.models import Repertoire
from flask_login import current_user, login_required

repertoire = Blueprint('repertoire', __name__)



@repertoire.route('/add-repertoire', methods=['GET', 'POST'])
@login_required
def add_repertoire():
    form = AddRepertoireForm()
    if form.validate_on_submit():
        new_rep = Repertoire(title=form.title.data, company=current_user)
        db.session.add(new_rep)
        db.session.commit()
        flash('Repertoire Added', 'success')
        return redirect(url_for('repertoire.add_repertoire'))
    elif request.method == 'GET':
        repertoire = Repertoire.query.filter_by(user_id=current_user.id)

    return render_template('add-repertoire.html', title='Add Repertoire', form=form, repertoire=repertoire)


@repertoire.route('/rep/<int:rep_id>', methods=['GET', 'POST'])
@login_required
def rep(rep_id):
    rep = Repertoire.query.get_or_404(rep_id)
    if rep.company != current_user:
        abort(403)
    
    return render_template('rep.html', title=rep.title, rep=rep)



@repertoire.route('/rehearsal-assignments', methods=['GET', 'POST'])
@login_required
def rehearsal_assignments():

    return render_template('rehearsal-assignments.html', title='Assignments')