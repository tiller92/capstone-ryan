from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, Email, Length

class UserLogin(FlaskForm):
  """Login form for users"""
  
  username = StringField('Username', validators=[DataRequired()])
  password = PasswordField('Password', validators=[DataRequired()])
  
class UserSignUp(FlaskForm):
  """Allow a new user to be added"""
  
  username = StringField('Username', validators=[DataRequired()])
  password = PasswordField('Password', validators=[DataRequired()])
  email = StringField('E-mail', validators=[DataRequired(), Email()])
  
class SignUpForm(FlaskForm):
  """Signs up a user"""
  username = StringField('Username', validators=[DataRequired()])
  password = PasswordField('Password', validators=[DataRequired()])
  email = StringField('E-mail', validators=[DataRequired(), Email()])
  

class AddWatched(FlaskForm):
  """add the info needed to track a congress member """
  first_name = StringField('First Name', validators=[DataRequired()])
  last_name = StringField('Last Name', validators=[DataRequired()])