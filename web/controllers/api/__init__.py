from flask import Blueprint

route_api = Blueprint('api_page', __name__)
from web.controllers.api.Member import *
from web.controllers.api.Collage import *
from web.controllers.api.Subject import *
from web.controllers.api.Plan import *
from web.controllers.api.Batch import *
from web.controllers.api.Level import *
from web.controllers.api.Search import *
from web.controllers.api.Application import *


@route_api.route("/")
def index():
    return "Mina Api V1.0"
