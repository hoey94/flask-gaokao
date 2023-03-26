# -*- coding: utf-8 -*-
from flask import Blueprint, g, request
from sqlalchemy import or_

from application import app
from common.libs.Helper import ops_render, iPagination
from common.models.User import User

route_index = Blueprint('index_page', __name__)


@route_index.route("/")
def index():
    current_user = g.current_user
    resp_data = {}
    query = User.query
    req = request.values
    page = int(req['p']) if ('p' in req and req['p']) else 1

    # 搜索功能
    if 'mix_kw' in req:
        rule = or_(User.nickname.ilike("%{0}%".format(req['mix_kw'])),
                   User.mobile.ilike("%{0}%".format(req['mix_kw'])))
        query = query.filter(rule)

    if 'status' in req and int(req['status']) > -1:
        query = query.filter(User.status == req['status'])

    # 分页功能
    page_params = {
        'total': query.count(),
        'page_size': app.config['PAGE_SIZE'],
        'page': page,
        'display': app.config['PAGE_DISPLAY'],
        'url': request.full_path.replace("&p={}".format(page), "")
    }
    pages = iPagination(page_params)
    offset = (page - 1) * app.config['PAGE_SIZE']
    limit = app.config['PAGE_SIZE'] * page

    list = query.order_by(User.uid.desc()).all()[offset:limit]
    resp_data['list'] = list
    resp_data['pages'] = pages
    resp_data['search_con'] = req
    resp_data['status_mapping'] = app.config['STATUS_MAPPING']

    return ops_render("account/index.html", resp_data)
