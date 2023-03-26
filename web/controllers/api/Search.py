from flask import jsonify, request
from sqlalchemy import or_

from web.controllers.api import route_api
from application import app, db
from common.models.CollageInfo.Collage import Collage


@route_api.route("/search/hot-list", methods=["GET"])
def getSearchHotList():
    resp = {'message': '获取成功', 'data': {}, 'success': True, 'code': 200}
    collage_list = Collage.query.order_by(Collage.order).limit(9).all()
    if not collage_list:
        resp['success'] = False
        resp['message'] = '获取失败'
        return jsonify(resp)

    data_collage_list = []
    index = 1
    for item in collage_list:
        dic = {'id': index, 'label': item.name}
        data_collage_list.append(dic)
        index += 1

    resp['data'] = {
        'list': data_collage_list
    }

    return jsonify(resp)


@route_api.route("/search", methods=["GET"])
def getSearchResult():
    resp = {'message': '获取成功', 'data': {}, 'success': True, 'code': 200}
    req = request.args
    q = req.get('q', '')
    if not q:
        resp['success'] = False
        resp['message'] = '获取失败'
        resp['code'] = -1
        return jsonify(resp)

    rule = or_(Collage.name.ilike("%{0}%".format(q)), Collage.e_name.ilike("%{0}%".format(q)),
               Collage.s_name.ilike("%{0}%".format(q)))
    collage_list = Collage.query.filter(rule).all()
    data_collage_list = []
    for item in collage_list:
        data_collage_list.append(item.to_dict())
    resp['data'] = {'list': data_collage_list}
    return jsonify(resp)
