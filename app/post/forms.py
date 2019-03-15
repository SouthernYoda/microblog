from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, SelectField, RadioField
from wtforms.validators import ValidationError, DataRequired, Length
from app.models import User

class PostForm(FlaskForm):
	post = TextAreaField('Say something',validators=[DataRequired(), Length(min=1, max=140)])
	visibility = RadioField('Visibility to others', choices=[('Private', 'Only visible to me'), ('Public', 'Visible to others')])
	submit = SubmitField('Submit')
