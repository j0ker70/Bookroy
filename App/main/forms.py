from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField


class SearchForm(FlaskForm):
    book_name = StringField('Book Name')
    max_price = IntegerField('Max Price')
    submit = SubmitField('Search')
