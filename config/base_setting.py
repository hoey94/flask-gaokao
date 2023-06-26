SERVER_PORT = 8999
DEBUG = False
JSON_AS_ASCII = False
SQLALCHEY_ECHO = False

# cookie认证管理员是否已登陆 key
AUTH_COOKIE_NAME = 'gaokao-guanliyuan'

# 过滤url认证拦截
IGNORE_URLS = [
    "^/user/login",
    "/api"
]

IGNORE_CHECK_LOGIN_URLS = [
    "^/static",
    "^/favicon.ico",
    "^/api"
]

# 分页
PAGE_SIZE = 5
PAGE_DISPLAY = 10

# 小程序分页
MINAPP_PAGE_SIZE = 20

# 分类字段
STATUS_MAPPING = {
    "1": "正常",
    "0": "已删除"
}

# 小程序相关设置
MINA_APP= {
    'appid': '*******',
    'appkey': '*********',
}

# 域名
APP = {
    'domain': 'http://10.1.44.246:8999/'
}

UPLOAD = {
    'ext': ['jpg', 'png', 'gif', 'jpeg','bmp'],
    'prefix_path': '/web/static/upload/',
    'prefix_url': '/static/upload/'
}

SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123456@127.0.0.1:3306/gaokao'
SQLALCHEMY_ECHO = True
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ENCODING = "utf-8"
DEBUG = True
SERVER_PORT = 8999
JSON_AS_ASCII = False