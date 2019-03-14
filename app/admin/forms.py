from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, SelectField, RadioField
from wtforms.validators import ValidationError, DataRequired, Email, Length
from app.models import User
#Author:Adam

class EditProfileForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired()])
	email = StringField('email', validators=[Email()])
	role = RadioField('role', choices=[('Admin','Administrator'),('User','Standard User')])
	#submit = SubmitField("action")

	def __init__(self, original_username, original_email, *args, **kwargs):
		super(EditProfileForm, self).__init__(*args,**kwargs)
		self.original_username = original_username
		self.original_email = original_email

	def validate_username(self, username):
		if username.data == self.original_username:
			return
		else:
			user = User.query.filter_by(username=self.username.data).first()
			if user is not None:
				raise ValidationError('Please use a different username.')

	def validate_email(self, email):
		if email.data == self.original_email:
			return
		else:
			user = User.query.filter_by(email=self.email.data).first()
			if user is not None:
				raise ValidationError('Please use a different email.')
