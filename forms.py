from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo

class IncidentForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    status = SelectField('Status', choices=[('open', 'Open'), ('closed', 'Closed')], validators=[DataRequired()])
    resolution_notes = TextAreaField('Resolution Notes', validators=[Length(max=500)])  # Optional field with a max length
    submit = SubmitField('Report Incident')

class UserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=150)])  # Added min length for username
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=35)])  # Added max length for password
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(max=150)])  # Same as UserForm
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=35)])  # Same as UserForm
    submit = SubmitField('Login')