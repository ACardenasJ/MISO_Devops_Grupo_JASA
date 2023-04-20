from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_restful import Api
from datetime import timedelta
import os
from modelos.modelos import db
from vistas import VistaConsultarBlackList, VistaCrearBlackList, VistaHealthCheck, VistaHealth

if 'DATABASE_URL' not in os.environ:
    DATABASE_URI = 'postgresql+psycopg2://postgres:DreamTeam123*@database-1.cazbca9jsbii.us-east-1.rds.amazonaws.com/postgres'
else:
    DATABASE_URI = os.environ['DATABASE_URL'] 
if DATABASE_URI is None or DATABASE_URI == '':
    DATABASE_URI = 'sqlite:///test.db'

print('DATABASE_URI:',DATABASE_URI)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'frase-secreta-blacklist'
app.config['PROPAGATE_EXCEPTIONS'] = True

app_context = app.app_context()
app_context.push()
db.init_app(app)
db.create_all()

cors = CORS(app)

api = Api(app)
api.add_resource(VistaCrearBlackList, '/blacklists')
api.add_resource(VistaConsultarBlackList, '/blacklists/<string:email>')
api.add_resource(VistaHealthCheck, '/blacklists/ping')
api.add_resource(VistaHealth, '/')

jwt = JWTManager(app)

print(' * BLACK LIST corriendo ----------------')

if __name__ == "__main__":
    PORT = 3000
    app.run(PORT, debug=True) 