# coding: utf-8
from sqlalchemy_serializer import SerializerMixin

from application import db


class SubjectGrade(db.Model, SerializerMixin):
    __tablename__ = 'subject-grade'

    id = db.Column(db.BigInteger, primary_key=True)
    collage_name = db.Column(db.String(255), nullable=False, server_default=db.FetchedValue())
    collage_id = db.Column(db.BigInteger, nullable=False)
    subject_name = db.Column(db.String(255), nullable=False)
    y_id = db.Column(db.BigInteger, nullable=False)
    year = db.Column(db.String(255), nullable=False)
    type = db.Column(db.String(255), nullable=False)
    batch = db.Column(db.String(255), nullable=False)
    min_grade = db.Column(db.Integer, nullable=False)
    min_level = db.Column(db.Integer, nullable=False)
    num = db.Column(db.Integer, nullable=False)
