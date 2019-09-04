from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField, StringField
from wtforms.validators import Optional, Length


class DescriptionForm(FlaskForm):
    description = TextAreaField('Description', validators=[Optional(), Length(0, 500)])
    submit = SubmitField()


class TagForm(FlaskForm):
    tag = StringField('Add Tag (usr space to separate)', validators=[Optional(), Length(0, 64)])
    submit = SubmitField()
