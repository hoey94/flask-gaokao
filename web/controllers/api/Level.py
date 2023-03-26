from flask import request, jsonify, g
import requests, json

from common.libs.Helper import getCurrentDate
from web.controllers.api import route_api
from application import app, db
from common.models.CollageInfo.Level import Level


@route_api.route("/level/list", methods=["GET"])
def getLevelList():
    resp = {'message': '获取成功', 'data': {}, 'success': True}
    req = request.args
    year = int(req.get('year', 2021))
    type = req.get('type', '理科')
    batch_list = Level.query.filter_by(year=year, type=type).all()
    data_batch_list = []
    for batch in batch_list:
        data_batch_list.append(batch.to_dict())
    resp['data'] = {'list': data_batch_list}

    return jsonify(resp)
