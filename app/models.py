from typing import List, Optional
from sqlalchemy import ForeignKey, PrimaryKeyConstraint, String, Integer
from sqlalchemy.orm import DeclarativeBase, relationship, mapped_column, Mapped, Session
from sqlalchemy import create_engine


class Base(DeclarativeBase):
    pass


# Création de la tables des utilisateurs
class Utilisateur(Base):
    __tablename__ = "utilisateur"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_name: Mapped[str] = mapped_column(String(30), unique=True)
    full_name: Mapped[str] = mapped_column(String(50))
    email_address: Mapped[String] = mapped_column(String(50), unique=True)
    password: Mapped[String] = mapped_column(String(50))
    role_id: Mapped[int] = mapped_column(ForeignKey("role.id"))
    role: Mapped["Role"] = relationship(back_populates="utilisateurs")
    commentaires: Mapped[List["Commentaire"]] = relationship(back_populates="utilisateur", cascade="all, delete-orphan")
    articles: Mapped[List["Article"]] = relationship(back_populates="utilisateur", cascade="all, delete-orphan")

    def __init__(self, user_name, full_name, email_address, password):
        self.user_name = user_name
        self.full_name = full_name
        self.email_address = email_address
        self.password = password

    def __repr__(self) -> str:
        return f"Utilisateur(id={self.id!r}, user_name={self.user_name!r}, fullname={self.full_name!r}, email_address={self.email_address!r}, role={self.role!r}, commentaires={self.commentaires!r})"


# les différents grades que les utilisateurs pourront avoir en en fonction des point
class Role(Base):
    __tablename__ = "role"

    id: Mapped[int] = mapped_column(primary_key=True)
    description: Mapped[str] = mapped_column(String(50))
    utilisateurs: Mapped[List["Utilisateur"]] = relationship(back_populates="role", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"{self.description}"


# les commentaires des différents articles
class Commentaire(Base):
    __tablename__ = "commentaire"

    id: Mapped[int] = mapped_column(primary_key=True)
    message: Mapped[str] = mapped_column(String(1024))
    id_utilisateur: Mapped[int] = mapped_column(ForeignKey("utilisateur.id"))
    id_article: Mapped[int] = mapped_column(ForeignKey("article.id"))
    utilisateur: Mapped["Utilisateur"] = relationship(back_populates="commentaires")
    article: Mapped["Article"] = relationship(back_populates="commentaires")

    def __init__(self, message, id_utilisateur, id_article):
        self.message = message
        self.id_utilisateur = id_utilisateur
        self.id_article = id_article

    def __repr__(self) -> str:
        return f"Commentaire : <br> {self.message!r} <br> <br>"


# les articles publié par les utilisateurs
class Article(Base):
    __tablename__ = "article"

    id: Mapped[int] = mapped_column(primary_key=True)
    titre: Mapped[str] = mapped_column(String(256))
    contenu: Mapped[str] = mapped_column(String(1024))
    id_utilisateur: Mapped[int] = mapped_column(ForeignKey("utilisateur.id"))
    utilisateur: Mapped["Utilisateur"] = relationship(back_populates="articles")
    commentaires: Mapped[List["Commentaire"]] = relationship(back_populates="article", cascade="all, delete-orphan")

    def __init__(self, titre, contenu, id_utilisateur):
        self.titre = titre
        self.contenu = contenu
        self.id_utilisateur = id_utilisateur

    def __repr__(self) -> str:
        return f"Article: <br> titre : {self.titre!r} <br> contenu : {self.contenu!r} <br> <br><br>"


engine = create_engine("sqlite:///app/data_base.db", echo=True)
# Base.metadata.create_all(engine)

# Administrateur : mail = masna.annour-ahmat@etu.amu.fr, mdp= announcement
# Modérateur : mail = victorhugo@flask.fr, mdp= victorhugo
# Abonne: mail : francois@flask.fr, mdp= francois
