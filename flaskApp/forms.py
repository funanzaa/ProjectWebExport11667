from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo



class LoginForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)],render_kw={"placeholder": "username"})
    password = PasswordField('Password', 
                            validators=[DataRequired()],render_kw={"placeholder": "password"})
    submit = SubmitField('Login')