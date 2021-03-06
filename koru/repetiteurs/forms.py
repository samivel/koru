from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField
from wtforms.validators import DataRequired




class AddRepetiteurForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])

    last_name = StringField('Last Name', validators=[DataRequired()])

    gender = RadioField(u'Gender', choices=[('Male'), ('Female'), ('Other')])

    submit = SubmitField('Submit')
