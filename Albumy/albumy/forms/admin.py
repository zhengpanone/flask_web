from wtforms import StringField, SelectField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError, Email

from albumy.models import Role, User
from albumy.forms.user import EditProfileForm


class EditProfileAdminForm(EditProfileForm):
    """
    管理员资料编辑表单
    """
    email = StringField('Email', validators=[DataRequired(), Length(1, 64), Email()])
    role = SelectField('Role', coerce=int)
    active = BooleanField('Active')
    confirmed = BooleanField('Confirmed')
    submit = SubmitField()

    def __init__(self, user, *args, **kwargs):
        super(EditProfileAdminForm, self).__init__(*args, **kwargs)
        self.role.choices = [(role.id, role.name)
                             for role in Role.query.order_by(Role.name).all()]
        self.user = user

    def validate_username(self, field):
        if field.data != self.user.username and User.query.filter_by(username=field.data).first():
            raise ValidationError("The username is already in use.")

    def validate_email(self, field):
        if field.data != self.user.email and User.query.filter_by(email=field.data).first():
            raise ValidationError("The email already in use.")
