from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, TextAreaField, validators
from wtforms.validators import DataRequired, Email
from app import app

app.config['SECRET_KEY'] = 'i_like_python'


# mon formulaire de login
class LoginForm(FlaskForm):
    email = EmailField(label='Email', validators=[DataRequired(), Email()])
    password = PasswordField(label='Mot de passe', validators=[DataRequired(), validators.length(min=8, max=20)])


# mon formulaire d'inscription
class RegisterForm(FlaskForm):
    firstname = StringField(label="Prenom", validators=[DataRequired()])
    lastname = StringField(label="Nom", validators=[DataRequired()])
    username = StringField(label="Nom d'utilisateur", validators=[DataRequired()])
    email = EmailField(label="Email", validators=[DataRequired(), Email()])
    password = PasswordField(label="Mot de passe", validators=[DataRequired(), validators.length(min=8, max=20),
                                                               validators.EqualTo('confirmation_password',
                                                                                  message="les mots de passe dooivent correspondre !")])
    confirmation_password = PasswordField(label="Confirmation du mot de passe", validators=[DataRequired()])


# mon formulaire pour écrire un article
class ArticleForm(FlaskForm):
    title = StringField(label="titre", validators=[DataRequired()])
    content = TextAreaField(label="Contenu", validators=[DataRequired()])


# mon formulaire pour écrire un commentaire
class CommentForm(FlaskForm):
    message = TextAreaField(label='Message', validators=[DataRequired()])


# mon formulaire pour la recherche article
class SearchForm(FlaskForm):
    search = StringField(label='Recherche')
