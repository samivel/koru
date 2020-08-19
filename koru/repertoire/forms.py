from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired




class AddRepertoireForm(FlaskForm):

    title = StringField('Title', validators=[DataRequired()])

    submit = SubmitField('Submit')
