from flask_wtf import FlaskForm
from wtforms import SubmitField, FileField
from wtforms.validators import DataRequired


class ImportFileForm(FlaskForm):
    file = FileField(validators=[DataRequired()])
    submit = SubmitField('SUBMIT')
