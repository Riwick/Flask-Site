from flask_wtf import FlaskForm
from wtforms.fields.simple import StringField, BooleanField, SubmitField, PasswordField, TextAreaField, TelField, FileField
from wtforms.validators import Email, DataRequired, Length, EqualTo


class LoginForm(FlaskForm):
    email = StringField(validators=[Email()])
    password = PasswordField(validators=[DataRequired(), Length(min=1, max=200)])
    remember = BooleanField("Запомнить меня", default=False)

    submit = SubmitField()


class RegisterForm(FlaskForm):
    username = StringField(validators=[DataRequired(), Length(min=1, max=200)])
    email = StringField(validators=[DataRequired(), Email()])
    phone = TelField(validators=[DataRequired(), Length(min=1, max=30)])
    password = PasswordField(validators=[DataRequired(), Length(min=1, max=200)])
    password_confirm = PasswordField(validators=[DataRequired(), Length(min=1, max=200),
                                                 EqualTo("password", message="Пароли не совпадают")])

    submit = SubmitField()


class FeedBackForm(FlaskForm):
    username = StringField(validators=[DataRequired(), Length(min=1, max=200)])
    phone = TelField(validators=[DataRequired(), Length(min=1, max=30)])
    email = StringField(validators=[DataRequired(), Email()])
    message = TextAreaField(validators=[DataRequired()])

    submit = SubmitField()
