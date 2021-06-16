from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, ValidationError, EqualTo, Email, Length

class SearchForm(FlaskForm):
    query = StringField('query', validators=[DataRequired(), Length(max=30)])
    submit = SubmitField('🔍')
