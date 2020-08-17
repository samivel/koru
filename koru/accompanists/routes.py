from flask import render_template, flash, redirect, url_for, request, abort, Blueprint
from koru import db
from koru.accompanists.forms import AddAccompanistForm
from koru.models import Accompanist
from flask_login import current_user, login_required

accompanists = Blueprint('accompanists', __name__)


@accompanists.route('/manage-accompanists', methods=['GET', 'POST'])
@login_required
def manage_accompanists():
    accompanists = Accompanist.query.filter_by(company=current_user).all()
    return render_template('/manage-accompanists.html', title='Accompanists', manageActive='active', accompanists=accompanists)




@accompanists.route('/add-accompanist', methods=['GET', 'POST'])
@login_required
def add_accompanist():
    form = AddAccompanistForm()
    if form.validate_on_submit():
        new_accompanist = Accompanist(first_name=form.first_name.data, last_name=form.last_name.data, gender=form.gender.data, company=current_user)
        db.session.add(new_accompanist)
        db.session.commit()
        flash('Accompanist Added', 'success')
        return redirect(url_for('accompanists.add_accompanist'))
    return render_template('/add-accompanist.html', title='Add Accompanist', addActive='active', form=form)



@accompanists.route('/accompanist/<int:accompanist_id>', methods=['GET', 'POST'])
@login_required
def accompanist(accompanist_id):
    accompanist = Accompanist.query.get_or_404(accompanist_id)
    if accompanist.company != current_user:
        abort(403)
    form = AddAccompanistForm()
    if form.validate_on_submit():
        accompanist.first_name = form.first_name.data
        accompanist.last_name = form.last_name.data
        accompanist.gender = form.gender.data
        db.session.commit()
        flash(f'{accompanist.first_name} updated', 'success')
        return redirect(url_for('accompanists.manage_accompanists'))
    elif request.method == 'GET':
        form.first_name.data = accompanist.first_name
        form.last_name.data = accompanist.last_name
        form.gender.data = accompanist.gender
    return render_template('accompanist.html', title=accompanist.first_name, manageActive='active', form=form, accompanist=accompanist)


@accompanists.route('/accompanist/<int:accompanist_id>/delete', methods=['POST'])
@login_required
def delete_accompanist(accompanist_id):
    accompanist = Accompanist.query.get_or_404(accompanist_id)
    if accompanist.company != current_user:
        abort(403)
    db.session.delete(accompanist)
    db.session.commit()
    flash(f'{accompanist.first_name} deleted', 'info')
    return redirect(url_for('accompanists.manage_accompanists'))