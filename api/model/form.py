from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, TelField, PasswordField, SubmitField, ValidationError, IntegerField, TextAreaField
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired, Length, Email, EqualTo
from model import storage


class RegistrationForm(FlaskForm):
    first_name = StringField('firstname', validators=[DataRequired(), Length(max=100)])

    last_name = StringField('lastname', validators=[DataRequired(), Length(max=100)])
    
    phone = TelField('tele', validators=[DataRequired()])

    email = StringField('Email', validators=[DataRequired(), Email()])

    birthdate = StringField('birthdate', render_kw={"placeholder": "DD/MM/YYYY"}, validators={DataRequired()})

    password = PasswordField('password', validators=[DataRequired(), Length(min=4)])

    confirm_password = PasswordField('confirm Password', validators=[DataRequired(), EqualTo('password')])

    submit = SubmitField('Sign Up')

    def validate_email(self, email):
        user_email = storage.query_email(email.data)
        if user_email:
            raise ValidationError('The User Email is already in use')

class LoginForm(FlaskForm):

    email = StringField('Email', validators=[DataRequired()])

    password = PasswordField('password', validators=[DataRequired()])

    submit = SubmitField('Login')

class UpdateForm(FlaskForm):
    first_name = StringField('firstname', validators=[DataRequired(), Length(max=100)])

    last_name = StringField('lastname', validators=[DataRequired(), Length(max=100)])
    
    phone = TelField('tele', validators=[DataRequired()])

    email = StringField('Email', validators=[DataRequired(), Email()])

    birthdate = StringField('birthdate', render_kw={"placeholder": "DD/MM/YYYY"}, validators={DataRequired()})

    submit = SubmitField('Update')

    def validate_email(self, email):
        if current_user.email != email.data:
            user_email = storage.query_email(email.data)
            if user_email:
                raise ValidationError('The User Email is already in use')
class UploadCv(FlaskForm):
    cv = FileField('Upload CV in PDF format', validators=[
        DataRequired(message='Please choose a file.'),
        FileAllowed(['pdf'], message='Only PDF files are allowed.')
    ])
    submit = SubmitField('Submit')

class PostForm(FlaskForm):
    title = StringField('Job title', validators=[DataRequired(), Length(max=200)])

    job_type = StringField('job type', validators=[DataRequired(), Length(max=100)])
    

    email = StringField('Your account Email', validators=[DataRequired(), Email()])

    location = StringField('location', validators={DataRequired()})

    level = StringField('level', validators=[DataRequired(), Length(max=200)])

    vacancies = IntegerField('vacancies', validators=[DataRequired()])

    salary = IntegerField('Salary')

    deadline = StringField('Application Deadline', render_kw={"placeholder": "DD/MM/YYYY"}, validators={DataRequired()})   
    
    description = TextAreaField('Job description', validators=[DataRequired(), Length(max=1000)])

    submit = SubmitField('Sign Up')

    def validate_email(self, email):
        
        if current_user.email != email.data:
            raise ValidationError('Please Use Your Own Account Email')