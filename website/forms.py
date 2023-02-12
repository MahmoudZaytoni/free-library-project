from flask_wtf import FlaskForm
from wtforms import EmailField, StringField, TextAreaField, PasswordField, SubmitField, FileField
from wtforms.validators import DataRequired, Length
from flask_wtf.file import FileRequired, FileAllowed

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

class BookForm(FlaskForm):
  title = StringField("Title:", validators=[DataRequired()])
  author = StringField("Author:", validators=[DataRequired()])
  cover = FileField("Cover:", validators=[FileRequired(), FileAllowed(['jpg', 'png'])])
  book = FileField("Book:", validators=[FileRequired(), FileAllowed(['pdf', 'txt'])])
  desc = TextAreaField("Description:")
  submit = SubmitField("Save")

class BookFormUpdate(BookForm):
  cover = FileField("Cover:", validators=[FileAllowed(['jpg', 'png'])])
  book = FileField("Book:", validators=[FileAllowed(['pdf', 'txt'])])