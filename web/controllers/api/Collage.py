from flask import request, jsonify, g
import requests, json
from sqlalchemy import or_

from common.libs.Helper import getCurrentDate
from web.controllers.api import route_api
from application import app, db
from common.models.CollageInfo.Collage import Collage
from common.models.CollageInfo.Province import Province
from common.models.CollageInfo.City import City


@route_api.route("/collage/hot", methods=["GET"])
def hotCollage():
    resp = {'message': '获取成功', 'data': {}, 'success': True, 'code': 200}
    hot_list = Collage.query.order_by(Collage.order).limit(20).all()
    if not hot_list:
        resp['success'] = False
        resp['message'] = '获取失败'
        return jsonify(resp)

    data_hot_list = []
    for item in hot_list:
        data_hot_list.append(item.to_dict())
        print(item.to_dict())

    resp['data'] = {
        'list': data_hot_list
    }

    return jsonify(resp)


@route_api.route("/collage/province", methods=["GET"])
def getProvinceList():
    """
    获取省份列表
    :return:
    """
    resp = {'message': '获取成功', 'data': {}, 'success': True, 'code': 200}
    province_list = Province.query.all()
    if not province_list:
        resp['success'] = False
        resp['message'] = '获取失败'
        return jsonify(resp)

    data_province_list = []
    for item in province_list:
        data_province_list.append(item.to_dict())
        print(item.to_dict())

    resp['data'] = {
        'list': data_province_list
    }

    return jsonify(resp)


@route_api.route("/collage/city", methods=["GET"])
def getCityList():
    """
    获取省份对应城市列表
    :return:
    """
    resp = {'message': '获取成功', 'data': {}, 'success': True, 'code': 200}
    req = request.args
    province_name = req.get('province', '')
    if not province_name:
        resp['success'] = False
        resp['message'] = '获取失败'
        resp['code'] = -1
        return jsonify(resp)

    rule = or_(Province.province.ilike("%{0}%".format(province_name)))
    province_id = Province.query.filter(rule).first().id

    if not province_id:
        resp['success'] = False
        resp['message'] = '获取失败'
        resp['code'] = -2
        return jsonify(resp)

    city_list = City.query.filter_by(province_id=int(province_id)).all()
    if not city_list:
        resp['success'] = False
        resp['message'] = '获取失败'
        resp['code'] = -3
        return jsonify(resp)

    data_city_list = []

    for city in city_list:
        data_city_list.append(city.to_dict())

    resp['data'] = {'list': data_city_list}
    return jsonify(resp)


@route_api.route("/collage/collage", methods=["GET"])
def getCollageList():
    """
    获取省份对应城市列表
    :return:
    """
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

    app.logger.debug(f'offset: {offset}, limit: {limit}')
    collage_list = query.all()[offset:limit]

    if not collage_list:
        resp['message'] = '没有数据'
        resp['code'] = -1
        resp['data']['has_more'] = False
        return jsonify(resp)

    data_collage_list = []

    for item in collage_list:
        data_collage_list.append(item.to_dict())

    resp['data'] = {
        'list': data_collage_list,
        'has_more': True
    }

    return jsonify(resp)
