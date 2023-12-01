from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email

class RegistroSuperusuarioForm(FlaskForm):
    username = StringField('Nombre de Usuario (Correo Electrónico)', validators=[DataRequired(), Email()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    submit = SubmitField('Registrar Superusuario')

class LoginForm(FlaskForm):
    username = StringField('Nombre de Usuario', validators=[DataRequired()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    submit = SubmitField('Iniciar Sesión')