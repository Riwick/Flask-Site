from flask_wtf import FlaskForm
from wtforms.fields.simple import StringField, SubmitField, TextAreaField, TelField
from wtforms.validators import Email, DataRequired, Length


class FeedBackForm(FlaskForm):
    username = StringField(validators=[DataRequired(), Length(min=1, max=200)])
    phone = TelField(validators=[DataRequired(), Length(min=1, max=30)])
    email = StringField(validators=[DataRequired(), Email()])
    message = TextAreaField(validators=[DataRequired()])

    submit = SubmitField()
