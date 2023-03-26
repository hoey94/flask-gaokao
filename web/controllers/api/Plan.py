from flask import request, jsonify, g
import requests, json
from sqlalchemy import or_

from common.libs.Helper import getCurrentDate
from common.models.CollageInfo.Collage import Collage
from web.controllers.api import route_api
from application import app, db
from common.models.CollageInfo.Plan import Plan


@route_api.route("/plan/list", methods=["GET"])
def getPlanCollageList():
    resp = {'message': '获取成功', 'data': {}, 'success': True, 'code': 200}
    req = request.args
    city = req.get('city', '')
    banxue = req.get('banxue', '')
    speacial = req.get('speacial', '')
    classify = req.get('classify', '')
    page = int(req.get('page', 0))

    query = Collage.query

    if city:
        rule = or_(Collage.city.ilike("%{0}%".format(city)))
        query = query.filter(rule)

    if banxue == '私立院校':
        query = query.filter_by(is_sili=1)
    elif banxue == '公立院校':
        query = query.filter_by(is_sili=0)

    if speacial == '985':
        query = query.filter_by(is_985=1)
    elif speacial == '211':
        query = query.filter_by(is_211=1)
    elif speacial == '重点院校':
        query = query.filter_by(is_zhongdian=1)

    if classify:
        rule = or_(Collage.c_classify.ilike("%{0}%".format(classify)))
        query = query.filter(rule)

    offset = page * app.config['MINAPP_PAGE_SIZE']
    limit = app.config['MINAPP_PAGE_SIZE'] * (page + 1)

    collage_list = query.all()

    if not collage_list:
        resp['message'] = '没有数据'
        resp['code'] = -1
        resp['data']['has_more'] = False
        return jsonify(resp)

    plan_list = []

    for item in collage_list[offset:limit]:
        plan_list = plan_list + Plan.query.filter_by(collage_id=item.id).all()

    data_plan_list = []

    for item in plan_list[offset:limit]:
        data_plan_list.append(item.to_dict())

    resp['data'] = {
        'list': data_plan_list,
        'has_more': True
    }

    return jsonify(resp)
