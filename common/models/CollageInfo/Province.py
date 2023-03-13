# coding: utf-8
from sqlalchemy_serializer import SerializerMixin

from application import db


class Province(db.Model, SerializerMixin):
    __tablename__ = 'province'
    serialize_rules = ("-is_deleted",)

    id = db.Column(db.Integer, primary_key=True)
    province = db.Column(db.String(100), nullable=False, unique=True)
    is_deleted = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
