from flask import request, redirect, g
import re

from application import app
from common.models.User import User
from common.libs.user.UserService import UserService
from common.libs.UrlManager import UrlManager
from common.libs.LogService import LogService


@app.before_request
def before_request():
    """
    检测登录拦截器
    :return: 继续请求
    """
    ignore_urls = app.config['IGNORE_URLS']
    ignore_check_login_urls = app.config['IGNORE_CHECK_LOGIN_URLS']

    path = request.path

    # 排除不需要检测的请求（登陆页面请求、api请求）
    pattern = re.compile("%s" % "|".join(ignore_check_login_urls))
    if pattern.match(path):
        return

    # 排除不需要检测的请求（静态资源请求、api请求）
    pattern = re.compile("%s" % "|".join(ignore_urls))
    if pattern.match(path):
        return

    if "/api" in path:
        return

    user_info = check_login()

    g.current_user = None

    if not user_info:
        return redirect(UrlManager.buildUrl("/user/login"))
    else:
        g.current_user = user_info

    # 添加日志
    LogService.addAccessLog()
    return


def check_login():
    """
    检查是否登录
    :return: 已登陆：当前登录对象，未登录：false
    """
    cookies = request.cookies
    auth_cookie = cookies[app.config['AUTH_COOKIE_NAME']] if app.config['AUTH_COOKIE_NAME'] in cookies else None
    if auth_cookie is None:
        return False

    # auth_cookie： AuthCode#uid
    auth_info = auth_cookie.split("#")
    if (len(auth_info)) != 2:
        return False

    try:
        user_info = User.query.filter_by(uid=auth_info[1]).first()
    except Exception:
        return False

    if user_info is None:
        return False

    if auth_info[0] != UserService.geneAuthCode(user_info):
        return False

    if user_info.status != 1:
        return False

    return user_info
