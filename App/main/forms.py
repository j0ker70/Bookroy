from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, TextAreaField
from wtforms.validators import DataRequired, Length


class SearchForm(FlaskForm):
    book_name = StringField('Book Name')
    max_price = IntegerField('Max Price')
    submit = SubmitField('Search')


class MessageForm(FlaskForm):
    message = TextAreaField('Message', validators=[
        DataRequired(), Length(min=0, max=140)])
    submit = SubmitField('Send')
