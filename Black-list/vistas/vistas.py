from modelos.modelos import ( Usuario, UsuarioSchema, db)
from datetime import datetime, timedelta
import hashlib
from flask import request
from flask_jwt_extended import create_access_token, jwt_required
from flask_restful import Resource

usuario_schema = UsuarioSchema()

def hash_pass(password: str, salt: str = None):
    if salt is None:
        salt = 'la-salt-es-esta'
    hash = hashlib.sha256(salt.encode('utf-8') + password.encode('utf-8')).hexdigest()
    return salt, hash

def verify_pass(password: str, hashed_password: str, salt: str):
    return hashlib.sha256(salt.encode('utf-8') + password.encode('utf-8')).hexdigest() == hashed_password

class VistaHealthCheck(Resource):
    def get(self):
        return 'pong', 200

class VistaInfoUsuario(Resource):
    def get(self):
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(' ')[1]
            usuario = Usuario.query.filter_by(token=token).first()
            if usuario and usuario.expireAt > datetime.now():
                return {'id':usuario.id, 'username':usuario.username, 'email':usuario.email}, 200
            else:
                return {'error': 'El token no es válido o está vencido.'}, 401
        return {'error': 'El token no está en el encabezado de la solicitud.'}, 400

class VistaBaseUsuario(Resource):
    def get(self):
        email_ = request.json.get('email', None)
        usuario = Usuario.query.filter_by(email=email_).first()
        if usuario:
            return {'id':usuario.id, 'username':usuario.username, 'email':usuario.email, 'status': usuario.state}, 200
        else:
            return {'error': 'No existe un usuario con ese correo electrónico. '}, 404

class VistaGeneracionToken(Resource):
    def post(self):
        username = request.json.get('username', None)
        password = request.json.get('password', None)
        if not username or not password:
            return {'error': 'Alguno de los campos no estan presentes en la solicitud.'}, 400
        usuario = Usuario.query.filter_by(username=username).first()
        if usuario:
            if(usuario.state == "VERIFICADO"):
                if verify_pass(password, usuario.password, usuario.salt):
                    access_token = create_access_token(identity=username)
                    now = datetime.now()
                    expiration_time = now + timedelta(minutes=30)
                    usuario.token = access_token
                    usuario.expireAt = expiration_time
                    db.session.commit()
                    return {'id':usuario.id,'token': access_token, "expireAt":str(expiration_time)}, 200
                else:
                    return {'error': 'Usuario o contraseña incorrectos'}, 404 
            else:
                return {'error': 'Usuario no está verificado'}, 404
        return {'error': 'Usuario no existe'}, 404

class VistaCrearUsuario(Resource):
    def post(self):
        username = request.json.get('username', None)
        email = request.json.get('email', None)
        password = request.json.get('password', None)
        if not username or not email or not password:
            return {'error': 'Alguno de los campos no estan presentes en la solicitud.'}, 400
        username = username.strip()
        if Usuario.query.filter_by(username=username).first() or Usuario.query.filter_by(email=email).first():
            return {'error': 'el usuario con el username o el correo ya existe'}, 412
        salt, hashed_pass = hash_pass(password)
        token = ''
        now = datetime.now()
        expireAt = now + timedelta(minutes=30)
        createdAt = now
        state = "POR_VERIFICAR"
        usuario = Usuario(username=username, 
                            email=email, 
                            password=hashed_pass, 
                            salt=salt, 
                            token=token, 
                            expireAt=expireAt, 
                            createdAt=createdAt, 
                            state=state)
        db.session.add(usuario)
        db.session.commit()
        return {'id':usuario.id, 'createdAt':str(usuario.createdAt)}, 201
    
    def put(self):
        user_id = request.json.get('id', None)
        state = request.json.get('status', None)
        if not user_id or not state:
            return {'error': 'Alguno de los campos no estan presentes en la solicitud.'}, 400
        state = request.json.get('status', None)
        if not user_id or not state:
            return {'error': 'Alguno de los campos no estan presentes en la solicitud.'}, 400
        user_buscado = Usuario.query.filter_by(id=int(user_id)).first()
        if not user_buscado:
            return {'error': 'el usuario no existe'}, 404
        user_buscado.state = state
        db.session.commit()
        return {'id':user_buscado.id, 'createdAt':str(user_buscado.createdAt), "email" :user_buscado.email , "email" :user_buscado.email }, 201