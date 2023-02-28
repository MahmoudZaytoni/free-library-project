from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, FileField
from wtforms.validators import DataRequired
from flask_wtf.file import FileRequired, FileAllowed
from wtforms_sqlalchemy.fields import QuerySelectField
from ..category.forms import category_query
from ..author.forms import author_query

class BookForm(FlaskForm):
  title = StringField("Title:", validators=[DataRequired()])
  author = QuerySelectField(query_factory=author_query, allow_blank=False, get_label='name')
  category = QuerySelectField(query_factory=category_query, allow_blank=True, get_label='category_name')
  cover = FileField("Cover:", validators=[FileRequired(), FileAllowed(['jpg', 'png'], message="File must be jpg or png")])
  book = FileField("Book:", validators=[FileRequired(), FileAllowed(['pdf', 'txt'], message="File must be pdf")])
  desc = TextAreaField("Description:")
  submit = SubmitField("Save")

class BookFormUpdate(BookForm):
  cover = FileField("Cover:", validators=[FileAllowed(['jpg', 'png'], message="File must be jpg or png")])
  book = FileField("Book:", validators=[FileAllowed(['pdf', 'txt'], message="File must be pdf")])