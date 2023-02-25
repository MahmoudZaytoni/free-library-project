from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from wtforms_sqlalchemy.fields import QuerySelectField
from ..models import Category

def category_query():
  return Category.query

class CategoryForm(FlaskForm):
  category = StringField("Category Name:", validators=[DataRequired()])
  submit = SubmitField("Save")

class FilterByCategory(FlaskForm):
  category = QuerySelectField(query_factory=category_query, allow_blank=True, get_label='category_name')
  apply = SubmitField("Apply")