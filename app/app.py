from flask import Flask
from config import Configuration #importation de la classe de configuration
from flask_bootstrap import Bootstrap


app = Flask(__name__)
# __name__ indique la racine de l'application pour retrouver les ressources
bootstrap = Bootstrap(app)

app.config.from_object(Configuration)
