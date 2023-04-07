from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_restful import Api
from datetime import timedelta
import os
from modelos.modelos import db
from vistas import VistaConsultarBlackList, VistaCrearBlackList, VistaHealthCheck, VistaHealth

DATABASE_URI = 'postgresql+psycopg2://postgres:DreamTeam123*@database-1.cazbca9jsbii.us-east-1.rds.amazonaws.com/postgres'

application = Flask(__name__)
application.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
application.config['JWT_SECRET_KEY'] = 'frase-secreta-blacklist'
application.config['PROPAGATE_EXCEPTIONS'] = True

app_context = application.app_context()
app_context.push()
db.init_app(application)
db.create_all()

cors = CORS(application)

api = Api(application)
api.add_resource(VistaCrearBlackList, '/blacklists')
api.add_resource(VistaConsultarBlackList, '/blacklists/<string:email>')
api.add_resource(VistaHealthCheck, '/blacklists/ping')
api.add_resource(VistaHealth, '/')

jwt = JWTManager(application)

print(' * BLACK LIST corriendo ----------------')

if __name__ == "__main__":
    PORT = 3000
    application.run(PORT, debug=True) 