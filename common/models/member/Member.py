# coding: utf-8
from application import db


class Member(db.Model):
    __tablename__ = 'member'

    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(100), nullable=False, server_default=db.FetchedValue())
    mobile = db.Column(db.String(11), nullable=False, server_default=db.FetchedValue())
    sex = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    avatar = db.Column(db.String(200), nullable=False, server_default=db.FetchedValue())
    salt = db.Column(db.String(32), nullable=False, server_default=db.FetchedValue())
    reg_ip = db.Column(db.String(100), nullable=False, server_default=db.FetchedValue())
    status = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    vip = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    updated_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    created_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    classify = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    normal = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    order = db.Column(db.String(15), nullable=False, server_default=db.FetchedValue())
    grade = db.Column(db.String(15), nullable=False, server_default=db.FetchedValue())
    year = db.Column(db.String(5), nullable=False, server_default=db.FetchedValue())

    @property
    def sex_desc(self):
        sex_mapping = {
            "0": "未知",
            "1": "男",
            "2": "女"
        }
        return sex_mapping[str(self.sex)]

    @property
    def classify_desc(self):
        classify_mapping = {
            "0": "理科",
            "1": "文科",
        }
        return classify_mapping[str(self.classify)]

    @property
    def normal_desc(self):
        classify_mapping = {
            "0": "艺术生",
            "1": "普通生",
        }
        return classify_mapping[str(self.normal)]
