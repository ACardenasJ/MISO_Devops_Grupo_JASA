from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_restful import Api
from datetime import timedelta
import os
from modelos.modelos import db

from vistas import VistaConsultarBlackList, VistaCrearBlackList, VistaHealthCheck

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blackList.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'frase-secreta'
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

jwt = JWTManager(app)

print(' * USER MANAGEMENT corriendo ----------------')

if __name__ == "__main__":
    HOST = '0.0.0.0'
    PORT = 3000
    app.run(HOST, PORT, debug=True) 