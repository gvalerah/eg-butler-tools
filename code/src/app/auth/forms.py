# source: app/auth/forms.py
from flask_wtf                          import FlaskForm
from wtforms                            import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators                 import Required, Length, Email, Regexp, EqualTo
from wtforms                            import ValidationError
#from emtec.collector.db.flask_models    import User
from emtec.butler.db.flask_models       import User

class LoginForm(FlaskForm):
    # GV 20181123 email = StringField('Email', validators=[Required(), Length(1, 64),    Email()])
    #username    = StringField('User Name', validators=[Required(), Length(1, 64)])
    username    = StringField('User Name', validators=[Required()])
    password    = PasswordField('Password', validators=[Required()])
    #remember_me = BooleanField('Keep me logged in')
    submit      = SubmitField('Log In')
    

class RegistrationForm(FlaskForm):
    username    = StringField('Username', validators=[ \
                    Required(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0, \
                    'Usernames must have only letters, ' \
                    'numbers, dots or underscores')])
                    
    role_id     = SelectField('Role', validators=[Required()], choices=[
        (1,'Solicitante'),
        (2,'Aprobador'),
        (3,'Visualizador'),
        (4,'Administrador'),
        (5,'Auditor')], 
        coerce=int)
        
    email       = StringField('Email', validators=[ Required(), Length(1, 64), Email()])
    
    password    = PasswordField('Password', validators=[ \
                    Required(), EqualTo('password2', message='Passwords must match.')])
    
    password2   = PasswordField('Confirm password', validators=[ Required()])
    
    submit = SubmitField('Register')
    
    #def validate_email(self, field):
    #    if User.query.filter_by(email=field.data).first():
    #        raise ValidationError('Email already registered.')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')
    

class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Old password', validators=[Required()])
    password = PasswordField('New password', validators=[
        Required(), EqualTo('password2', message='Passwords must match')])
    password2 = PasswordField('Confirm new password', validators=[Required()])
    submit = SubmitField('Update Password')


class PasswordResetRequestForm(FlaskForm):
    email = StringField('Email', validators=[Required(), Length(1, 64),
                                             Email()])
    submit = SubmitField('Reset Password')


class PasswordResetForm(FlaskForm):
    email = StringField('Email', validators=[Required(), Length(1, 64),
                                             Email()])
    password = PasswordField('New Password', validators=[
        Required(), EqualTo('password2', message='Passwords must match')])
    password2 = PasswordField('Confirm password', validators=[Required()])
    submit = SubmitField('Reset Password')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first() is None:
            raise ValidationError('Unknown email address.')


class ChangeEmailForm(FlaskForm):
    email = StringField('New Email', validators=[Required(), Length(1, 64),
                                                 Email()])
    password = PasswordField('Password', validators=[Required()])
    submit = SubmitField('Update Email Address')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')      
