from flask import render_template, flash, redirect, url_for, request, abort, Blueprint
from koru import db
from koru.bms.forms import AddBalletMasterForm
from koru.models import BalletMaster
from flask_login import current_user, login_required


bms = Blueprint('bms', __name__)


@bms.route('/manage-balletMasters', methods=['GET', 'POST'])
@login_required
def manage_balletMasters():
    bms = BalletMaster.query.filter_by(user_id=current_user.id)

    return render_template('manage-balletMasters.html', title='Manage Ballet Masters', manageActive='active', bms=bms)



@bms.route('/add-balletMaster', methods=['GET', 'POST'])
@login_required
def add_balletMaster():
    form = AddBalletMasterForm()
    # If form validates, creates a new bm instance with the provided values
    if form.validate_on_submit():
        new_bm = BalletMaster(first_name=form.first_name.data, last_name=form.last_name.data, gender=form.gender.data, company=current_user)
        db.session.add(new_bm)
        db.session.commit()

        flash('Ballet Master successfully added', 'success')
        return redirect(url_for('bms.add_balletMaster'))
        
    return render_template('add-balletMaster.html', title='Add Ballet Master', addActive='active', form=form)


@bms.route('/ballet-master/<int:bm_id>', methods=['GET', 'POST'])
@login_required
def ballet_master(bm_id):
    # Query db for bm matching the id passed in with url get
    bm = BalletMaster.query.get_or_404(bm_id)
    # Ensure bm belongs to user
    if bm.company != current_user:
        abort(403)
    # Render page to manage bm
    form = AddBalletMasterForm()
    # Assigns user provided values to the bm instance
    if form.validate_on_submit():
        bm.first_name = form.first_name.data
        bm.last_name = form.last_name.data
        bm.gender = form.gender.data
        db.session.commit()
        flash('Ballet Master Updated', 'success')
        return redirect(url_for('bms.manage_balletMasters'))
    elif request.method == 'GET':
        # Fills the form with the bm info when page rendered via GET
        form.first_name.data = bm.first_name
        form.last_name.data = bm.last_name
        
        form.gender.data = bm.gender
    return render_template('ballet-master.html', title=bm.first_name, bm=bm, manageActive='active', form=form)


@bms.route('/ballet-master/<int:bm_id>/delete', methods=['POST'])
@login_required
def delete_bm(bm_id):
    bm = BalletMaster.query.get_or_404(bm_id)
    if bm.company != current_user:
        abort(403)
    db.session.delete(bm)
    db.session.commit()
    flash('Ballet Master Deleted', 'info')
    return redirect(url_for('bms.manage_balletMasters'))