from models import Utilisateur, engine, Article, Commentaire
from sqlalchemy.orm import Session
from sqlalchemy import select


def create_user(user_name, lastname, firstname, email, password):
    with Session(engine) as session:
        user = Utilisateur(user_name, lastname + " " + firstname, email, password)
        user.role_id = 1
        session.add(user)
        session.commit()


def authentification(email, password):
    session = Session(engine)
    usr_password = session.scalars(select(Utilisateur.password).where(Utilisateur.email_address == email)).first()
    if usr_password == password:
        return True
    return False


def create_article(title, content, user_id):
    with Session(engine) as session:
        article = Article(title, content, user_id)
        session.add(article)
        session.commit()
    return article


def create_comment(content, user_id, article_id):
    with Session(engine) as session:
        comment = Commentaire(content, user_id, article_id)
        session.add(comment)
        session.commit()


