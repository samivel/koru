
from flask import render_template, flash, redirect, url_for, request, abort, Blueprint
from koru import db
from koru.dancers.forms import AddDancerForm
from koru.models import Dancer
from flask_login import current_user, login_required




dancers = Blueprint('dancers', __name__)



@dancers.route('/manage-dancers', methods=['GET', 'POST'])
@login_required
def manage_dancers():
    # Query db for all dancers belonging to the user to display in order of rank first, then gender the last name
    principal_dancers = Dancer.query.filter_by(user_id=current_user.id).filter(Dancer.rank=='Principal').order_by(Dancer.gender, Dancer.last_name).all()
    first_soloist_dancers = Dancer.query.filter_by(user_id=current_user.id).filter(Dancer.rank=='First Soloist').order_by(Dancer.gender, Dancer.last_name).all()
    second_soloist_dancers = Dancer.query.filter_by(user_id=current_user.id).filter(Dancer.rank=='Second Soloist').order_by(Dancer.gender, Dancer.last_name).all()
    corps_dancers = Dancer.query.filter_by(user_id=current_user.id).filter(Dancer.rank=='Corps de Ballet').order_by(Dancer.gender, Dancer.last_name).all()
    apprentice_dancers = Dancer.query.filter_by(user_id=current_user.id).filter(Dancer.rank=='Apprentice/2nd Company').order_by(Dancer.gender, Dancer.last_name).all()


    return render_template('manage-dancers.html', title='Manage Dancers', manageActive='active', principal_dancers=principal_dancers, first_soloist_dancers=first_soloist_dancers,
                                                        second_soloist_dancers=second_soloist_dancers, corps_dancers=corps_dancers, apprentice_dancers=apprentice_dancers)



@dancers.route('/add-dancer', methods=['GET', 'POST'])
@login_required
def add_dancer():
    form = AddDancerForm()
    # If form validates, creates a new dancer instance with the provided values
    if form.validate_on_submit():
        new_dancer = Dancer(first_name=form.first_name.data, last_name=form.last_name.data, rank=form.rank.data, gender=form.gender.data, company=current_user)
        db.session.add(new_dancer)
        db.session.commit()

        flash('Dancer successfully added', 'success')
        return redirect(url_for('dancers.add_dancer'))
        
    return render_template('add-dancer.html', title='Add dancers', dancerActive='active', form=form)



@dancers.route('/dancer/<int:dancer_id>', methods=['GET', 'POST'])
@login_required
def dancer(dancer_id):
    # Query db for dancer matching the id passed in with url get
    dancer = Dancer.query.get_or_404(dancer_id)
    # Ensure dancer belongs to user
    if dancer.company != current_user:
        abort(403)
    # Render page to manage dancer
    form = AddDancerForm()
    # Assigns user provided values to the dancer instance
    if form.validate_on_submit():
        dancer.first_name = form.first_name.data
        dancer.last_name = form.last_name.data
        dancer.rank = form.rank.data
        dancer.gender = form.gender.data
        db.session.commit()
        flash('Dancer Updated', 'success')
        return redirect(url_for('dancers.manage_dancers'))
    elif request.method == 'GET':
        # Fills the form with the dancers info when page rendered via GET
        form.first_name.data = dancer.first_name
        form.last_name.data = dancer.last_name
        form.rank.data = dancer.rank
        form.gender.data = dancer.gender
    return render_template('dancer.html', title=dancer.first_name, dancer=dancer, manageActive='active', form=form)


@dancers.route('/dancer/<int:dancer_id>/delete', methods=['POST'])
@login_required
def delete_dancer(dancer_id):
    # Query db for dancer matching the id passed in with url get
    dancer = Dancer.query.get_or_404(dancer_id)
    # Ensure dancer belongs to user
    if dancer.company != current_user:
        abort(403)
    #Delete dancer from database and redirect
    db.session.delete(dancer)
    db.session.commit()
    flash('Dancer deleted', 'info')
    return redirect(url_for('dancers.manage_dancers'))
