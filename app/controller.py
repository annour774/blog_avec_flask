from sqlalchemy.orm import Session
from models import engine, Role, Commentaire, Article, Utilisateur
from sqlalchemy import select

# pour créer des rôles
# with Session(engine) as session:
#     abonne = Role(description="Abonne")
#     moderateur = Role(description="Modérateur")
#     administrateur = Role(description="Administrateur")
#     session.add_all([abonne, moderateur, administrateur])
#     session.commit()

# pour lire le contenu de la tables rôle
# session = Session(engine)

# stmt = select(Utilisateur)
# for role in session.scalars(stmt):
#     print(role)

# admin = session.get(Utilisateur, 2)
# admin.role_id = 2
# session.commit()
#
#
# print(admin.role)


