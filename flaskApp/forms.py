from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flaskApp.models import web_user



class RegistrationForm(FlaskForm):
    username = StringField('Username:', validators=[DataRequired(), Length(min=2, max=20)], render_kw={"placeholder": "Username"})
    email = StringField('Email:',
                        validators=[DataRequired(), Email()], render_kw={"placeholder": "Email"})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={"placeholder": "Password"})
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')], render_kw={"placeholder": "Confirm Password"})
    submit = SubmitField('Register')

    def validate_username(self, username):

        user = web_user.query.filter_by(username=username.data).first()   

        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):

        user = web_user.query.filter_by(email=email.data).first()

        if user:
            raise ValidationError('That email is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()], render_kw= {"placeholder": "Username"})
    password = PasswordField('Password', validators=[DataRequired()] , render_kw= {"placeholder": "Password"})
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')