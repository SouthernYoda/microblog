from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, SelectField, RadioField
from wtforms.validators import ValidationError, DataRequired, Length
from app.models import User
