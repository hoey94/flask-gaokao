# coding: utf-8
from sqlalchemy_serializer import SerializerMixin

from application import db


class Batch(db.Model, SerializerMixin):
    __tablename__ = 'batch'

    id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    batch = db.Column(db.String(255), nullable=False, server_default=db.FetchedValue())
    grade = db.Column(db.Integer, nullable=False)
    type = db.Column(db.String(255), nullable=False, server_default=db.FetchedValue())
