# 拦截器
from web.controllers.api import route_api
from web.interceptors.Authinterceptor import *
from web.interceptors.ErrorInterceptor import *
from web.interceptors.ApiAuthinterceptor import *

from application import app
# 蓝图
from web.controllers.index import route_index
from web.controllers.static import route_static
from web.controllers.user.User import route_user
from web.controllers.account.Account import route_account

app.register_blueprint(route_index, url_prefix='/')
app.register_blueprint(route_user, url_prefix='/user')
app.register_blueprint(route_static, url_prefix="/static")
app.register_blueprint(route_account, url_prefix="/account")
app.register_blueprint(route_api, url_prefix="/api")
