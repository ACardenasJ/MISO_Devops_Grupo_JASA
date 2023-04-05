from modelos.modelos import ( BlackList, BlackListSchema, db)
from datetime import datetime, timedelta
from flask import request

from flask_restful import Resource

blackList_schema = BlackListSchema()

class VistaHealthCheck(Resource):
    def get(self):
        return 'pong', 200

class VistaConsultarBlackList(Resource):
    def get(self, email):
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(' ')[1]
            #email_ = request.json.get('email', None)
            email_in_blackList = BlackList.query.filter_by(email=email).first()
            if email_in_blackList:
                return {'id':email_in_blackList.id, 'email':email_in_blackList.email}, 200
            else:
                return {'error': 'el email no está en la lista negra.'}, 401
        return {'error': 'El token no está en el encabezado de la solicitud.'}, 400

class VistaCrearBlackList(Resource):
    def post(self):
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(' ')[1]
            email = request.json.get('email', None)
            app_uuid = request.json.get('app_uuid', None)
            blocked_reason = request.json.get('blocked_reason', None)
            ipSolicitud = request.remote_addr
            if not email or not app_uuid or not blocked_reason:
                return {'error': 'Uno o Alguno de los campos no estan presentes en la solicitud.'}, 400  
            if not ipSolicitud:
                return {'error': 'No puede obtener la Ip de la Solicitud.'}, 400
            if BlackList.query.filter_by(email=email).first():
                return {'error': 'El email ya se encuentra en la lista negra'}, 412
            now = datetime.now()
            createdAt = now
            blackList = BlackList(email=email, 
                                app_uuid=app_uuid, 
                                blocked_reason=blocked_reason, 
                                createdAt=createdAt, 
                                ipSolicitud=ipSolicitud)
            db.session.add(blackList)
            db.session.commit()
            return {'id':blackList.id, 'email:': blackList.email,'createdAt':str(blackList.createdAt)}, 201
        return {'error': 'El token no está en el encabezado de la solicitud.'}, 400
