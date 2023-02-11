from flask_wtf import FlaskForm
from wtforms import EmailField, StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length


class LoginForm(FlaskForm):
  email = EmailField("Email", validators=[DataRequired(), Length(min=4)])
  password = PasswordField("Password", validators=[DataRequired(), Length(min=7)])
  submit = SubmitField("Submit")

class SignUpForm(FlaskForm):
  email = EmailField("Email", validators=[DataRequired(), Length(min=4)])
  first_name = StringField("First Name", validators=[DataRequired(), Length(min=3)])
  password1 = PasswordField("Password", validators=[DataRequired(), Length(min=7)])
  password2 = PasswordField("Confirm Password", validators=[DataRequired(), Length(min=7)])
  submit = SubmitField("Create Account")
