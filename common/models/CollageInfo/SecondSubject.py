# coding: utf-8
from sqlalchemy_serializer import SerializerMixin

from application import db


class SecondSubject(db.Model, SerializerMixin):
    __tablename__ = 'second_subject'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255))
    name = db.Column(db.String(255))
