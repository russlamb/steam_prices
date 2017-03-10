from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField
from wtforms.validators import DataRequired

class SteamItemForm(FlaskForm):
    item_name = StringField('this_item', validators=[DataRequired()])
    #remember_me = BooleanField('remember_me', default=False) 