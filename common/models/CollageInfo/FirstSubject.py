# coding: utf-8
from sqlalchemy_serializer import SerializerMixin

from application import db


class FirstSubject(db.Model, SerializerMixin):
    __tablename__ = 'first_subject'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
