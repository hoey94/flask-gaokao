# coding: utf-8
from sqlalchemy_serializer import SerializerMixin

from application import db


class Plan(db.Model, SerializerMixin):
    __tablename__ = 'plan'

    id = db.Column(db.BigInteger, primary_key=True)
    collage_name = db.Column(db.String(64), nullable=False)
    collage_id = db.Column(db.BigInteger, nullable=False, server_default=db.FetchedValue())
    type = db.Column(db.String(255), nullable=False, server_default=db.FetchedValue())
    subject = db.Column(db.String(255), nullable=False, server_default=db.FetchedValue())
    batch = db.Column(db.String(255), nullable=False, server_default=db.FetchedValue())
    year = db.Column(db.String(10), nullable=False, server_default=db.FetchedValue())
    cost = db.Column(db.String(64), nullable=False, server_default=db.FetchedValue())
    num = db.Column(db.Integer, nullable=False)
