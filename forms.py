from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, Email, Length

class UserLogin(FlaskForm):
  """Login form for users"""
  
  username = StringField('Username', validators=[DataRequired()])
 
  
class UserSignUp(FlaskForm):
  """Allow a new user to be added"""
  
  username = StringField('Username', validators=[DataRequired()])
  email = StringField('E-mail', validators=[DataRequired(), Email()])
  

  