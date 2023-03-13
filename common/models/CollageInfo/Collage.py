# coding: utf-8
from sqlalchemy_serializer import SerializerMixin

from application import db


class Collage(db.Model, SerializerMixin):
    __tablename__ = 'collage'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False, unique=True, server_default=db.FetchedValue())
    e_name = db.Column(db.String(100), nullable=False, server_default=db.FetchedValue())
    s_name = db.Column(db.String(100))
    province_id = db.Column(db.Integer)
    province = db.Column(db.String(64), server_default=db.FetchedValue())
    city_id = db.Column(db.Integer, nullable=False)
    city = db.Column(db.String(20), nullable=False, server_default=db.FetchedValue())
    created_year = db.Column(db.String(64), nullable=False, server_default=db.FetchedValue())
    local_org = db.Column(db.String(50), nullable=False, server_default=db.FetchedValue())
    is_yishu = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    is_985 = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    is_211 = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    is_zhongdian = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    is_sili = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    order = db.Column(db.BigInteger, nullable=False, server_default=db.FetchedValue())
    phone = db.Column(db.String(255), nullable=False, server_default=db.FetchedValue())
    email = db.Column(db.String(255), nullable=False, server_default=db.FetchedValue())
    url = db.Column(db.String(255), nullable=False, server_default=db.FetchedValue())
    address = db.Column(db.String(255), nullable=False)
    code = db.Column(db.String(10), nullable=False)
    classify = db.Column(db.String(255), nullable=False, server_default=db.FetchedValue())
    c_classify = db.Column(db.String(255), nullable=False, server_default=db.FetchedValue())
