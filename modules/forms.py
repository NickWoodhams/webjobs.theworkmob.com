from flask.ext.wtf import Form
from wtforms import TextField, PasswordField, validators, TextAreaField, SelectField, SelectMultipleField, HiddenField, RadioField, BooleanField, FileField
from wtforms.validators import ValidationError, Required, Optional
import re

__all__ = ['searchForm']


class searchForm(Form):
    search = TextField('Search term', [Required])
    excluded = TextField('Excluded terms', [Optional])
    include_body = BooleanField('Search body?', [Optional])
