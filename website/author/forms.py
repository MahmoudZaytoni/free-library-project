from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, FileField
from wtforms.validators import DataRequired
from flask_wtf.file import FileAllowed
from ..models import Author

def author_query():
  return Author.query

class AuthorForm(FlaskForm):
  name = StringField('Author Name:', validators=[DataRequired()])
  photo = FileField("photo:", validators=[FileAllowed(['jpg', 'png'], message="File must be jpg or png")])
  desc = TextAreaField("Description:", validators=[DataRequired()])
  submit = SubmitField("save")