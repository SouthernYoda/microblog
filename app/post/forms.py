from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, SelectField, RadioField
from wtforms.validators import ValidationError, DataRequired, Length
from app.models import User

class PostForm(FlaskForm):
	title = StringField('Title', validators=[DataRequired(), Length(min=1, max=20)])
	body = TextAreaField('Content:',validators=[DataRequired(), Length(min=1, max=1000)], render_kw={'class': 'form-control', 'rows': 40})
	visibility = RadioField('Visibility to others', choices=[('Private', 'Only visible to me'), ('Public', 'Visible to others')], validators=[DataRequired()])
	submit = SubmitField('Post')
