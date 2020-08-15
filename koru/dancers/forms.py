
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField
from wtforms.validators import DataRequired




class AddDancerForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])

    last_name = StringField('Last Name', validators=[DataRequired()])

    rank = RadioField(u'Rank', choices=[('Principal'), ('First Soloist'), ('Second Soloist'), ('Corps de Ballet'), ('Apprentice/2nd Company')])

    gender = RadioField(u'Gender', choices=[('Male'), ('Female'), ('Other')])

    submit = SubmitField('Submit')

