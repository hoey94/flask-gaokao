from flask import request, jsonify, g
import requests, json

from common.libs.Helper import getCurrentDate
from web.controllers.api import route_api
from application import app, db
from common.models.member.Member import Member
from common.models.member.OauthMemberBind import OauthMemberBind
from common.models.member.WxShareHistory import WxShareHistory
from common.libs.member.MemberService import MemberService


@route_api.route("/member/login", methods=["GET", "POST"])
def login():
    resp = {'message': '', 'data': {}, 'success': True}
    req = request.values
    openid = req['openid'] if 'openid' in req else None
    # 换了新的接口，那就更简单了

    if openid is None or len(openid) < 1:
        resp['success'] = False
        resp['message'] = "调用微信出错"
        return jsonify(resp)

    nickname = req['nickName'] if 'nickName' in req else ''
    sex = req['gender'] if 'gender' in req else 0
    avatar = req['avatarUrl'] if 'avatarUrl' in req else ''
    '''
        判断是否已经测试过，注册了直接返回一些信息
    '''
    bind_info = OauthMemberBind.query.filter_by(openid=openid, type=1).first()
    if not bind_info:
        model_member = Member()
        model_member.nickname = nickname
        model_member.sex = sex
        model_member.avatar = avatar
        model_member.salt = MemberService.geneSalt()
        model_member.updated_time = model_member.created_time = getCurrentDate()
        db.session.add(model_member)
        db.session.commit()

        model_bind = OauthMemberBind()
        model_bind.member_id = model_member.id
        model_bind.type = 1
        model_bind.openid = openid
        model_bind.extra = ''
        model_bind.updated_time = model_bind.created_time = getCurrentDate()
        db.session.add(model_bind)
        db.session.commit()

        bind_info = model_bind

    member_info = Member.query.filter_by(id=bind_info.member_id).first()
    token = "%s#%s" % (MemberService.geneAuthCode(member_info), member_info.id)
    memberInfo = {
        'nickName': member_info.nickname,
        'avatarUrl': member_info.avatar,
        'order': member_info.order,
        'grade': member_info.grade,
        'classify': member_info.classify,
        'normal': member_info.normal,
        'mobile': member_info.mobile,
        'year': member_info.year
    }
    resp['data'] = {
        'token': token,
        'userInfo': memberInfo
    }
    return jsonify(resp)


@route_api.route("/member/openid", methods=["POST"])
def getOpenid():
    """
    获取openid
    :return:
    """
    resp = {'message': '获取成功', 'data': {}, 'success': True}
    req = request.values
    code = req['code'] if 'code' in req else ''
    if not code or len(code) < 1:
        resp['success'] = False
        resp['message'] = "需要code"
        return jsonify(resp)

    openid = MemberService.getWeChatOpenId(code)
    if openid is None:
        resp['success'] = False
        resp['message'] = "调用微信服务出错"
        return jsonify(resp)

    resp['data'] = {'openid': openid}
    return jsonify(resp)


@route_api.route("/member/nickname", methods=["POST"])
def editNickname():
    """
    修改会员昵称
    :return:
    """
    resp = {'message': '修改成功', 'data': {}, 'success': True, 'code': 200}
    req = request.values
    token = req['token'] if 'token' in req else None
    nickname = req['nickname'] if 'nickname' in req else None
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

    member_info = Member.query.filter_by(id=t_list[1]).first()

    if not member_info:
        resp['success'] = False
        resp['message'] = "找不到该用户"
        resp['code'] = -1
        return jsonify(resp)

    if t_list[0] != MemberService.geneAuthCode(member_info):
        resp['success'] = False
        resp['message'] = "找不到该用户"
        resp['code'] = -1
        return jsonify(resp)

    if not nickname:
        resp['success'] = False
        resp['message'] = "未输入昵称"
        resp['code'] = -1
        return jsonify(resp)

    member_info.nickname = nickname
    member_info.updated_time = getCurrentDate()
    db.session.add(member_info)
    db.session.commit()

    memberInfo = {
        'nickName': member_info.nickname,
        'avatarUrl': member_info.avatar,
        'order': member_info.order,
        'grade': member_info.grade,
        'classify': member_info.classify,
        'normal': member_info.normal,
        'mobile': member_info.mobile,
        'year': member_info.year
    }
    resp['data'] = {'userInfo': memberInfo}
    return jsonify(resp)


@route_api.route("/member/mobile", methods=["POST"])
def editMobile():
    """
    修改会员手机号
    :return:
    """
    resp = {'message': '修改成功', 'data': {}, 'success': True, 'code': 200}
    req = request.values
    token = req['token'] if 'token' in req else None
    mobile = req['mobile'] if 'mobile' in req else None
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

    member_info = Member.query.filter_by(id=t_list[1]).first()

    if not member_info:
        resp['success'] = False
        resp['message'] = "找不到该用户"
        resp['code'] = -1
        return jsonify(resp)

    if t_list[0] != MemberService.geneAuthCode(member_info):
        resp['success'] = False
        resp['message'] = "找不到该用户"
        resp['code'] = -1
        return jsonify(resp)

    if not mobile:
        resp['success'] = False
        resp['message'] = "未输入手机号"
        resp['code'] = -1
        return jsonify(resp)

    member_info.mobile = mobile
    member_info.updated_time = getCurrentDate()
    db.session.add(member_info)
    db.session.commit()

    memberInfo = {
        'nickName': member_info.nickname,
        'avatarUrl': member_info.avatar,
        'order': member_info.order,
        'grade': member_info.grade,
        'classify': member_info.classify,
        'normal': member_info.normal,
        'mobile': member_info.mobile,
        'year': member_info.year
    }
    resp['data'] = {'userInfo': memberInfo}
    return jsonify(resp)


@route_api.route("/member/studentInfo", methods=["POST"])
def editStudentInfo():
    """
    修改学生信息
    :return:
    """
    resp = {'message': '修改成功', 'data': {}, 'success': True, 'code': 200}
    req = request.values
    token = req['token'] if 'token' in req else None
    classify = int(req['classify']) if 'classify' in req else -1
    normal = int(req['normal']) if 'normal' in req else -1
    order = req['order'] if 'order' in req else None
    grade = req['grade'] if 'grade' in req else None
    year = req['year'] if 'year' in req else None

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

    member_info = Member.query.filter_by(id=t_list[1]).first()

    if not member_info:
        resp['success'] = False
        resp['message'] = "找不到该用户"
        resp['code'] = -1
        return jsonify(resp)

    if t_list[0] != MemberService.geneAuthCode(member_info):
        resp['success'] = False
        resp['message'] = "找不到该用户"
        resp['code'] = -1
        return jsonify(resp)

    if classify < 0:
        resp['success'] = False
        resp['message'] = "请选择选科"
        resp['code'] = -1
        return jsonify(resp)

    if normal < 0:
        resp['success'] = False
        resp['message'] = "请选择考生类别"
        resp['code'] = -1
        return jsonify(resp)

    if not order:
        resp['success'] = False
        resp['message'] = "未输入位次"
        resp['code'] = -1
        return jsonify(resp)

    if not grade:
        resp['success'] = False
        resp['message'] = "未输入成绩"
        resp['code'] = -1
        return jsonify(resp)

    if not year:
        resp['success'] = False
        resp['message'] = "为选择年份"
        resp['code'] = -1
        return jsonify(resp)

    member_info.classify = classify
    member_info.normal = normal
    member_info.order = order
    member_info.grade = grade
    member_info.year = year
    member_info.updated_time = getCurrentDate()
    db.session.add(member_info)
    db.session.commit()

    memberInfo = {
        'nickName': member_info.nickname,
        'avatarUrl': member_info.avatar,
        'order': member_info.order,
        'grade': member_info.grade,
        'classify': member_info.classify,
        'normal': member_info.normal,
        'mobile': member_info.mobile,
        'year': member_info.year
    }
    resp['data'] = {'userInfo': memberInfo}
    return jsonify(resp)


@route_api.route("/member/share", methods=["POST"])
def memberShare():
    resp = {'code': 200, 'msg': '分享成功', 'data': {}}
    req = request.values
    url = req['url'] if 'url' in req else None
    member_info = g.member_info
    model_share = WxShareHistory()
    model_share.share_url = url
    model_share.created_time = getCurrentDate()
    if member_info:
        model_share.member_id = member_info.id

    db.session.add(member_info)
    db.session.commit()
    return jsonify(resp)
