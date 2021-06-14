from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField,SelectField,IntegerField,FloatField 
from wtforms.validators import DataRequired, Length, Email, EqualTo,ValidationError
from mainapp.models import User

class RegistrationForm(FlaskForm): 
    nom = StringField('Nom',validators=[DataRequired(), Length(min=2, max=20)])
    prenom = StringField('Prenom',validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',validators=[DataRequired(), Email()])
    password = PasswordField('Mot de passe', validators=[DataRequired()])
    niveau = SelectField(choices=[('Premiere'), ('Deuxieme'),('Troisieme')],validators=[DataRequired()])
    specialite = SelectField(choices=[('IDL'),('IDISC'),('ISEOAC') ],validators=[DataRequired()])
    submit = SubmitField('Ajouter')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')

class UpdateUserForm(FlaskForm):
    nom = StringField('Nom',validators=[DataRequired(), Length(min=2, max=20)])
    prenom = StringField('Prenom',validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',validators=[DataRequired(), Email()])
    password = PasswordField('Mot de passe', validators=[DataRequired()])
    niveau = SelectField(choices=[('Premiere'), ('Deuxieme'),('Troisieme')],validators=[DataRequired()])
    specialite = SelectField(choices=[('IDL'),('IDISC'),('ISEOAC') ],validators=[DataRequired()])
    submit = SubmitField('Modifier')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')

class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Mot de passe', validators=[DataRequired()])
    remember = BooleanField('Souviens-Vous')
    submit = SubmitField('Connecter')

class MatiereForm(FlaskForm): 
    nom = StringField('Nom',validators=[DataRequired(), Length(min=2, max=40)])
    niveau = SelectField(choices=[('Premiere'), ('Deuxieme'),('Troisieme')],validators=[DataRequired()])
    specialite = SelectField(choices=[('IDL'),('Idisc'),('Iseoac') ],validators=[DataRequired()])
    module = StringField('Module',validators=[DataRequired(), Length(min=2, max=40)])
    coefficient = FloatField('Coefficient',validators=[DataRequired()])
    submit = SubmitField('Ajouter')

class ReaserchForm(FlaskForm): 
    semestre = SelectField(choices=[(1), (2)],validators=[DataRequired()])
    niveau = SelectField(choices=[('Premiere'), ('Deuxieme'),('Troisieme')],validators=[DataRequired()])
    specialite = SelectField(choices=[('IDL'),('Idisc'),('Iseoac') ],validators=[DataRequired()])
    submit = SubmitField('RECHERCHER')

