from flask import request, jsonify, g
import requests, json
from sqlalchemy import or_

from common.libs.Helper import getCurrentDate
from common.libs.member.MemberService import MemberService
from common.models.application.Application import Application
from common.models.member.Member import Member
from web.controllers.api import route_api
from application import app, db
from common.models.application.YuCe import Yuce
from common.libs.application.ApplicationService import ApplicationService


@route_api.route("/application/list", methods=["GET"])
def getApplicationList():
    resp = {'message': '获取成功', 'data': {}, 'success': True, 'code': 200}
    req = request.args
    grade = int(req.get('grade', -1))
    column = req.get('column', '')
    token = req.get('token', '')

    if not token:
        resp['success'] = False
        resp['message'] = "token传递错误"
        resp['code'] = -1
        return jsonify(resp)

    t_list = token.split("#")

    if len(t_list) != 2:
        resp['success'] = False
        resp['message'] = "token传递错误"
        resp['code'] = -2
        return jsonify(resp)

    application_info = Application.query.filter_by(member_id=t_list[1]).all()

    add_list = []

    if application_info:
        for item in application_info:
            add_list.append(item.y_id)

    if not column:
        resp['success'] = False
        resp['code'] = -1
        resp['message'] = '错误！'
        return jsonify(resp)

    if grade < 0:
        resp['success'] = False
        resp['code'] = -1
        resp['message'] = '请传入正确的成绩'
        return jsonify(resp)
    applicationService = ApplicationService()

    if column == '冲一冲':
        resp['data']['list'] = applicationService.getFirstList(grade, add_list)
    elif column == '稳一稳':
        resp['data']['list'] = applicationService.getMiddleList(grade, add_list)
    else:
        resp['data']['list'] = applicationService.getLastList(grade, add_list)
    return jsonify(resp)


@route_api.route("/application/add", methods=["POST"])
def addApplication():
    resp = {'message': '获取成功', 'data': {}, 'success': True, 'code': 200}
    req = request.values
    y_id = int(req['y_id']) if 'y_id' in req else -1
    token = req['token'] if 'token' in req else None

    if y_id < 0:
        resp['success'] = False
        resp['code'] = -1
        resp['message'] = '请传入正确的成绩'
        return jsonify(resp)

    if not token:
        resp['success'] = False
        resp['message'] = "token传递错误"
        resp['code'] = -1
        return jsonify(resp)

    t_list = token.split("#")

    if len(t_list) != 2:
        resp['success'] = False
        resp['message'] = "token传递错误"
        resp['code'] = -2
        return jsonify(resp)

    application_info = Application.query.filter_by(member_id=t_list[1]).all()
    add_list = []
    if application_info:
        for item in application_info:
            add_list.append(item.y_id)

    if y_id in add_list:
        resp['data'] = {'success': True}
        return jsonify(resp)
    else:
        application_data = Application()
        application_data.y_id = y_id
        application_data.member_id = t_list[1]
        db.session.add(application_data)
        db.session.commit()
        resp['data'] = {'success': True}
        return jsonify(resp)


@route_api.route("/application/get", methods=["GET"])
def getMemBerApplicationList():
    resp = {'message': '获取成功', 'data': {}, 'success': True, 'code': 200}
    req = request.args
    token = req.get('token', '')

    if not token:
        resp['success'] = False
        resp['message'] = "token传递错误"
        resp['code'] = -1
        return jsonify(resp)

    t_list = token.split("#")

    if len(t_list) != 2:
        resp['success'] = False
        resp['message'] = "token传递错误"
        resp['code'] = -2
        return jsonify(resp)

    application_info = Application.query.filter_by(member_id=t_list[1]).all()
    y_id_list = []
    if application_info:
        for item in application_info:
            y_id_list.append(item.y_id)

    Yuce_list = []
    if y_id_list:
        for item in y_id_list:
            Yuce_list.append(Yuce.query.filter_by(id=int(item)).first().to_dict())

    resp['data'] = {'list': Yuce_list}
    return jsonify(resp)

@route_api.route("/application/drop", methods=["POST"])
def dropMemBerApplicationList():
    resp = {'message': '获取成功', 'data': {}, 'success': True, 'code': 200}
    req = request.values
    y_id = int(req['y_id']) if 'y_id' in req else -1

    token = req['token'] if 'token' in req else None

    if y_id < 0:
        resp['success'] = False
        resp['code'] = -1
        resp['message'] = '请传入正确的成绩'
        return jsonify(resp)

    if not token:
        resp['success'] = False
        resp['message'] = "token传递错误"
        resp['code'] = -1
        return jsonify(resp)

    t_list = token.split("#")

    if len(t_list) != 2:
        resp['success'] = False
        resp['message'] = "token传递错误"
        resp['code'] = -2
        return jsonify(resp)

    application_info = Application.query.filter_by(member_id=t_list[1],y_id=y_id).first()

    if application_info:
        db.session.delete(application_info)
        db.session.commit()
        resp['data'] = {'success': True}
        return jsonify(resp)
    else:
        resp['data'] = {'success': True}
        return jsonify(resp)