from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_restful import Api
from datetime import timedelta
import os
from modelos.modelos import db

from vistas import VistaCrearUsuario, VistaGeneracionToken, VistaInfoUsuario, VistaHealthCheck, VistaBaseUsuario

DATABASE_URI = os.environ['DATABASE_URL'] 
if DATABASE_URI is None or DATABASE_URI == '':
    DATABASE_URI = 'sqlite:///test_user.db'

print(DATABASE_URI)
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'frase-secreta'
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=30)
app.config['PROPAGATE_EXCEPTIONS'] = True

app_context = app.app_context()
app_context.push()
db.init_app(app)
db.create_all()

cors = CORS(app)

api = Api(app)
api.add_resource(VistaCrearUsuario, '/users/')
api.add_resource(VistaBaseUsuario, '/user_base')
api.add_resource(VistaGeneracionToken, '/users/auth')
api.add_resource(VistaInfoUsuario, '/users/me')
api.add_resource(VistaHealthCheck, '/users/ping')

jwt = JWTManager(app)

print(' * USER MANAGEMENT corriendo ----------------')

if __name__ == "__main__":
    HOST = '0.0.0.0'
    PORT = 3000
    app.run(HOST, PORT, debug=True) 