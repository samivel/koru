from flask import render_template, flash, redirect, url_for, request, abort, Blueprint
from koru import db
from koru.repetiteurs.forms import AddRepetiteurForm
from koru.models import Repetiteur
from flask_login import current_user, login_required

repetiteurs = Blueprint('repetiteurs', __name__)


@repetiteurs.route('/manage-repetiteurs', methods=['GET', 'POST'])
@login_required
def manage_repetiteurs():
    repetiteurs = Repetiteur.query.filter_by(company=current_user).all()
    return render_template('/manage-repetiteurs.html', title='Repetiteurs', manageActive='active', repetiteurs=repetiteurs)

@repetiteurs.route('/add-repetiteur', methods=['GET', 'POST'])
@login_required
def add_repetiteur():
    form = AddRepetiteurForm()
    if form.validate_on_submit():
        new_repetiteur = Repetiteur(first_name=form.first_name.data, last_name=form.last_name.data, gender=form.gender.data, company=current_user)
        db.session.add(new_repetiteur)
        db.session.commit()
        flash('Repetiteur Added', 'success')
        return redirect(url_for('repetiteurs.add_repetiteur'))
    return render_template('/add-repetiteur.html', title='Add Repetiteur', addActive='active', form=form)

@repetiteurs.route('/repetiteur/<int:repetiteur_id>', methods=['GET', 'POST'])
@login_required
def repetiteur(repetiteur_id):
    repetiteur = Repetiteur.query.get_or_404(repetiteur_id)
    if repetiteur.company != current_user:
        abort(403)
    form = AddRepetiteurForm()
    if form.validate_on_submit():
        repetiteur.first_name = form.first_name.data
        repetiteur.last_name = form.last_name.data
        repetiteur.gender = form.gender.data
        db.session.commit()
        flash(f'{repetiteur.first_name} updated', 'success')
        return redirect(url_for('repetiteurs.manage_repetiteurs'))
    elif request.method == 'GET':
        form.first_name.data = repetiteur.first_name
        form.last_name.data = repetiteur.last_name
        form.gender.data = repetiteur.gender
    return render_template('/repetiteur.html', title=repetiteur.first_name, manageActive='active', form=form, repetiteur=repetiteur)



@repetiteurs.route('/repetiteur/<int:repetiteur_id>/delete', methods=['POST'])
@login_required
def delete_repetiteur(repetiteur_id):
    repetiteur = Repetiteur.query.get_or_404(repetiteur_id)
    if repetiteur.company != current_user:
        abort(403)
    db.session.delete(repetiteur)
    db.session.commit()
    flash(f'{repetiteur.first_name} deleted', 'info')
    return redirect(url_for('repetiteurs.manage_repetiteurs'))