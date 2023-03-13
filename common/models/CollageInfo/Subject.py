# coding: utf-8
from sqlalchemy_serializer import SerializerMixin

from application import db


class Subject(db.Model, SerializerMixin):
    __tablename__ = 'subject'

    id = db.Column(db.BigInteger, primary_key=True)
    first_name = db.Column(db.String(64), nullable=False, server_default=db.FetchedValue())
    second_name = db.Column(db.String(64), nullable=False, server_default=db.FetchedValue())
    third_name = db.Column(db.String(64), nullable=False, server_default=db.FetchedValue())
    type = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    grant = db.Column(db.String(64), nullable=False, server_default=db.FetchedValue())
    close = db.Column(db.String(255), nullable=False, server_default=db.FetchedValue())
    code = db.Column(db.String(64), nullable=False, server_default=db.FetchedValue())
