# coding: utf-8
from sqlalchemy_serializer import SerializerMixin

from application import db


class Application(db.Model, SerializerMixin):
    __tablename__ = 'application'

    id = db.Column(db.BigInteger, primary_key=True)
    member_id = db.Column(db.BigInteger, nullable=False)
    y_id = db.Column(db.BigInteger, nullable=False)
