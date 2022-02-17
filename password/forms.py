from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.widgets import PasswordInput
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, URL, Optional
from password.models import User
from flask_login import current_user

class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class UpdateAccountForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Update')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')

class PasswordForm(FlaskForm):
    website = StringField('Website', validators=[DataRequired(), URL()])
    name = StringField('Name')
    email = StringField('Email', validators=[Optional(), Email()])
    username = StringField('Username')
    password = StringField('Password', validators=[DataRequired()], widget=PasswordInput(hide_value=False), id='password')
    show_password = BooleanField('Show password', id='check', render_kw={"onclick": "myFunction()"})
    submit = SubmitField('Save')

    
    def validate(self):
        if not super().validate():
            return False
        result = True
        seen = set()
        for field in [self.email, self.username]:
            if field.data in seen:
                self.email.errors.append('Please enter either an email or username.')
                self.username.errors.append('Please enter either an email or username.')
                result = False
            else:
                seen.add(field.data)
        return result