from flask import request, jsonify, g
import requests, json
from sqlalchemy import or_

from common.libs.Helper import getCurrentDate
from web.controllers.api import route_api
from application import app, db
from common.models.CollageInfo.FirstSubject import FirstSubject
from common.models.CollageInfo.Subject import Subject
from common.models.CollageInfo.SecondSubject import SecondSubject


@route_api.route("/subject/hot", methods=["GET"])
def hotSubject():
    resp = {'message': '获取成功', 'data': {}, 'success': True, 'code': 200}
    hot_list = Subject.query.limit(20).all()
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

@route_api.route("/subject/first", methods=["GET"])
def getFirstSubject():
    """
        获取省份列表
        :return:
        """
    resp = {'message': '获取成功', 'data': {}, 'success': True, 'code': 200}
    first_subject_list = FirstSubject.query.all()
    if not first_subject_list:
        resp['success'] = False
        resp['message'] = '获取失败'
        return jsonify(resp)

    data_first_subject_list = []
    for item in first_subject_list:
        data_first_subject_list.append(item.to_dict())
        print(item.to_dict())

    resp['data'] = {
        'list': data_first_subject_list
    }

    return jsonify(resp)


@route_api.route("/subject/second", methods=["GET"])
def getSecondList():
    """
    获取省份对应城市列表
    :return:
    """
    resp = {'message': '获取成功', 'data': {}, 'success': True, 'code': 200}
    req = request.args
    first = req.get('first', '')
    if not first:
        resp['success'] = False
        resp['message'] = '获取失败'
        resp['code'] = -1
        return jsonify(resp)

    rule = or_(SecondSubject.first_name.ilike("%{0}%".format(first)))
    second_list = SecondSubject.query.filter(rule).all()

    if not second_list:
        resp['success'] = False
        resp['message'] = '获取失败'
        resp['code'] = -3
        return jsonify(resp)

    data_second_list = []

    for city in second_list:
        data_second_list.append(city.to_dict())

    resp['data'] = {'list': data_second_list}
    return jsonify(resp)


@route_api.route("/subject/subject", methods=["GET"])
def getSubjectList():
    resp = {'message': '获取成功', 'data': {}, 'success': True, 'code': 200}
    req = request.args
    subject = req.get('subject', '')
    type = req.get('type', '')
    page = int(req.get('page', 0))

    query = Subject.query

    if subject:
        rule = or_(Subject.second_name.ilike("%{0}%".format(subject)))
        query = query.filter(rule)

    if type == '本科':
        query = query.filter_by(type=0)
    elif type == '专科':
        query = query.filter_by(type=1)

    offset = page * app.config['MINAPP_PAGE_SIZE']
    limit = app.config['MINAPP_PAGE_SIZE'] * (page + 1)

    app.logger.debug(f'offset: {offset}, limit: {limit}')
    subject_list = query.all()[offset:limit]

    if not subject_list:
        resp['message'] = '没有数据'
        resp['code'] = -1
        resp['data']['has_more'] = False
        return jsonify(resp)

    data_subject_list = []

    for item in subject_list:
        data_subject_list.append(item.to_dict())

    resp['data'] = {
        'list': data_subject_list,
        'has_more': True
    }

    return jsonify(resp)
