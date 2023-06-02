from flask_sqlalchemy import SQLAlchemy
from marshmallow import fields, Schema
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from sqlalchemy import Column, Integer, String


db = SQLAlchemy()

class BlackList(db.Model):
    __tablename__ = 'blackList'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50))
    app_uuid = db.Column(db.String(50))
    blocked_reason = db.Column(db.String(255))
    createdAt = db.Column(db.DateTime)
    ipSolicitud = db.Column(db.String(50))


class BlackListSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = BlackList
        include_relationships = True
        load_instance = True