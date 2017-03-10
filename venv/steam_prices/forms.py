from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, IntegerField
from wtforms.validators import DataRequired, Optional

class SteamItemForm(FlaskForm):
    item_name = StringField('this_item', validators=[DataRequired()])
    days=IntegerField("14", validators=[Optional()])
    #remember_me = BooleanField('remember_me', default=False) 