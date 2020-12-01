from flask_wtf import FlaskForm
from wtforms import ValidationError
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.fields import (
    PasswordField,
    StringField,
    SubmitField,
)
from wtforms.fields.html5 import EmailField
from wtforms.validators import (
    Email,
    EqualTo,
    InputRequired,
    Length,
)

from app import db
from app.models import User


class NewUserForm(FlaskForm):
    role = StringField(
        'New account type',
        validators=[InputRequired(), Length(1, 64)])
    username = StringField(
        'Username', validators=[InputRequired(),
                                  Length(1, 64)])
    username = StringField(
        'Name', validators =[ Length(1, 64)])
    password = PasswordField(
        'Password',
        validators=[
            InputRequired()])

    submit = SubmitField('Create')


class ChangeUsernameForm(FlaskForm):
    username = StringField(
        'New username', validators=[InputRequired(),
                                 Length(1, 64)])
    submit = SubmitField('Update Username')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('username already registered.')


class ChangeAccountTypeForm(FlaskForm):
    role = StringField(
        'New account type',
        validators=[InputRequired(), Length(1, 64)])
    submit = SubmitField('Update role')


class ChangePasswordForm(FlaskForm):
    password = PasswordField(
        'New password', validators=[InputRequired(),
                                    Length(1, 64)])
    submit = SubmitField('Update Password')
