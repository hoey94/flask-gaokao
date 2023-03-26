# coding: utf-8
from sqlalchemy_serializer import SerializerMixin

from application import db


class Yuce(db.Model, SerializerMixin):
    __tablename__ = 'yuce'

    id = db.Column(db.BigInteger, primary_key=True)
    collage_name = db.Column(db.String(255), nullable=False, server_default=db.FetchedValue())
    subject_name = db.Column(db.String(255), nullable=False, server_default=db.FetchedValue())
    type = db.Column(db.String(255), nullable=False)
    is_delete = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    y_grade = db.Column(db.Integer, nullable=False)
    y_classify = db.Column(db.Integer)
