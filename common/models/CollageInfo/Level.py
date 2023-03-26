# coding: utf-8
from sqlalchemy_serializer import SerializerMixin

from application import db


class Level(db.Model, SerializerMixin):
    __tablename__ = 'level'

    id = db.Column(db.BigInteger, primary_key=True)
    year = db.Column(db.String(10), nullable=False, server_default=db.FetchedValue())
    type = db.Column(db.String(10), nullable=False, server_default=db.FetchedValue())
    grade = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    num = db.Column(db.Integer, nullable=False)
    total = db.Column(db.Integer, nullable=False)
