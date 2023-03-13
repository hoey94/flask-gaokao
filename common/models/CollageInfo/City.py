# coding: utf-8
from sqlalchemy_serializer import SerializerMixin

from application import db


class City(db.Model, SerializerMixin):
    __tablename__ = 'city'
    serialize_rules = ("-is_deleted",)

    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(200), nullable=False, index=True)
    province_id = db.Column(db.Integer, nullable=False)
    is_deleted = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
