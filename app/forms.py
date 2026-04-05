from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FileField
from wtforms.validators import InputRequired
from flask_wtf.file import FileRequired, FileAllowed



# Movie Form

class MovieForm(FlaskForm):
  title = StringField('Title', validators=[InputRequired()])
  description = TextAreaField('Description', validators=[InputRequired()])
  poster = FileField('Poster', validators=[FileRequired(), FileAllowed(['jpg', 'png'], "Only JPG and PNG images are allowed")])