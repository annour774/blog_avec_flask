import markdown
import markdown.extensions.fenced_code
from flask import render_template, redirect, url_for, session, flash
from forms import LoginForm, RegisterForm, ArticleForm, CommentForm, SearchForm
from handler import create_user, authentification, create_article, create_comment
from app import app
from sqlalchemy import select
from models import Utilisateur, engine, Role, Article, Commentaire
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.orm import sessionmaker

SESSION = sessionmaker(bind=engine)
current_session = Session(engine)

MODERATEUR_NB_ARTICLE = 50


@app.route("/home")
def homepage():
    return redirect(url_for("afficher_articles"))


@app.route('/welcome')
def welcome_page():
    email = session["user"]
    user_id = current_session.scalars(select(Utilisateur.id).where(Utilisateur.email_address == email)).first()
    user = current_session.get(Utilisateur, user_id)
    nb_article = len(user.articles)
    if nb_article >= MODERATEUR_NB_ARTICLE and user.role_id == 1:
        user.role_id = 2
        current_session.commit()
    return render_template('welcome.html', user_name=user.user_name)


@app.route("/", methods=['GET', 'POST'])
def connexion():
    form = LoginForm()
    if form.validate_on_submit():
        if authentification(form.email.data, form.password.data):
            session['user'] = form.email.data
            flash("You've been logged in successfully")
            return redirect(url_for('welcome_page'))
        flash("L'adresse mail ou le mot de passe est incorrect !")
    return render_template("Connexion.html", form=form)


@app.route('/inscription', methods=['GET', 'POST'])
def inscription():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data == form.confirmation_password.data:
            create_user(form.username.data, form.lastname.data, form.firstname.data, form.email.data,
                        form.password.data)
            flash("Accound created successfully !")
            return redirect(url_for('connexion'))
        redirect(url_for("inscription"))
    return render_template('inscription.html', form=form)


@app.route('/deconnexion')
def deconnexion():
    flash("You've been logged out succesfully")
    session.pop('user', None)
    return redirect(url_for('connexion'))


@app.route('/home/profile')
def profile():
    email = session["user"]
    user_name = current_session.scalars(select(Utilisateur.id).where(Utilisateur.email_address == email)).first()
    user = current_session.get(Utilisateur, user_name)
    return render_template('profile.html', full_name=user.full_name, username=user.user_name, role=user.role,
                           role_id=user.role_id, user_id=user.id)


@app.route('/home/contact')
def contact():
    return render_template('contact.html')


@app.route('/home/nouvelle_article', methods=['GET', 'POST'])
def ecrire_article():
    form = ArticleForm()
    if form.validate_on_submit():
        title = form.title.data
        email = session["user"]
        user_id = current_session.scalars(select(Utilisateur.id).where(Utilisateur.email_address == email)).first()
        html = markdown.markdown(form.content.data, extensions=['fenced_code', 'codehilite'])
        create_article(title, html, user_id)
        flash("Article Created successfully !")
        return redirect(url_for(('afficher_mes_postes')))
    return render_template('ecrire_article.html', form=form)


@app.route('/afficher_articles')
def afficher_articles():
    articles = current_session.query(Article).all()
    email = session["user"]
    user_id = current_session.scalars(select(Utilisateur.id).where(Utilisateur.email_address == email)).first()
    user = current_session.get(Utilisateur, user_id)
    return render_template("afficher_article.html", articles=articles, mes_postes=False, user_role_id=user.role_id)


@app.route('/home/articles/<int:article_id>/comments/nouveau_commentaire', methods=['GET', 'POST'])
def ecrire_commentaire(article_id):
    form = CommentForm()
    if form.validate_on_submit():
        email = session['user']
        user_id = current_session.scalars(select(Utilisateur.id).where(Utilisateur.email_address == email)).first()
        html_content = markdown.markdown(form.message.data, extensions=['fenced_code', 'codehilite'])
        create_comment(html_content, user_id, article_id)
        return redirect(url_for('afficher_commentaires', article_id=article_id))
    return render_template('ecrire_commetaire.html', form=form, article_id=article_id)


@app.route("/articles/<int:article_id>/commentaires", methods=['GET', 'POST'])
def afficher_commentaires(article_id):
    commentaires = current_session.query(Commentaire).filter(Commentaire.id_article == article_id).all()
    email = session['user']
    user_id = current_session.scalars(select(Utilisateur.id).where(Utilisateur.email_address == email)).first()
    return render_template('afficher_commentaire.html', commentaires=commentaires, article_id=article_id, user_id=user_id)


@app.route('/home/mes_postes')
def afficher_mes_postes():
    email = session['user']
    user_id = current_session.scalars(select(Utilisateur.id).where(Utilisateur.email_address == email)).first()
    user = current_session.get(Utilisateur, user_id)
    articles = current_session.query(Article).filter(Article.id_utilisateur == user_id).all()
    return render_template('afficher_article.html', articles=articles, mes_postes=True, user_role_id=user.role_id)


@app.route('/home/recherche', methods=['GET', 'POST'])
def recherche():
    email = session["user"]
    user_id = current_session.scalars(select(Utilisateur.id).where(Utilisateur.email_address == email)).first()
    user = current_session.get(Utilisateur, user_id)
    form = SearchForm()
    if form.validate_on_submit():
        mot_cle = form.search.data.lower()
        tous_les_articles = current_session.query(Article).options(joinedload(Article.utilisateur)).all()
        articles_selectione = []
        for article in tous_les_articles:
            if mot_cle in article.titre.lower() or mot_cle in article.contenu.lower():
                articles_selectione.append(article)
        return render_template('afficher_article.html', articles=articles_selectione, user_role_id=user.role_id)
    return render_template('recherche.html', form=form)


@app.route("/home/mes_postes/<int:article_id>")
def supprimer_article(article_id):
    article = current_session.get(Article, article_id)
    current_session.delete(article)
    current_session.commit()
    flash("Article deleted successfully !")
    return redirect(url_for('afficher_articles'))


@app.route("/<int:user_id>/delete_account")
def supprimer_compte(user_id):
    email = session["user"]
    current_user_id = current_session.scalars(select(Utilisateur.id).where(Utilisateur.email_address == email)).first()
    user_to_delete = current_session.get(Utilisateur, user_id)
    current_session.delete(user_to_delete)
    current_session.commit()
    flash("Account deleted successfully !")
    if user_id == current_user_id:
        return redirect(url_for("connexion"))
    return redirect(url_for('afficher_comptes'))


@app.route("/comments/<int:comment_id>/delete_comment")
def supprimer_commentaire(comment_id):
    comment = current_session.get(Commentaire, comment_id)
    article_id = comment.id_article
    current_session.delete(comment)
    current_session.commit()
    flash("Comment deleted successfully!")
    return redirect(url_for("afficher_commentaires", article_id=article_id))


@app.route("/home/profile/acounts")
def afficher_comptes():
    email = session["user"]
    user_id = current_session.scalars(select(Utilisateur.id).where(Utilisateur.email_address == email)).first()
    users = current_session.query(Utilisateur).filter(Utilisateur.id != user_id).all()
    return render_template("afficher_comptes.html", users=users)
