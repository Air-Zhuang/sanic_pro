from sanic import Blueprint

from sanic.exceptions import NotFound
from sanic.response import text

bp_v1 = Blueprint('bp_v1',url_prefix='/v1')    #给蓝图起名，慎重

'''=========================middleware==============================================='''
@bp_v1.middleware
async def print_on_request(request):
    print("bp_middleware")

@bp_v1.middleware('request')
async def halt_request(request):
    print("bp_middleware --> request")

@bp_v1.middleware('response')
async def halt_response(request, response):
    print("bp_middleware --> request")
    # response.headers["Server"] = "Fake-Server"        #中间件可以修改请求
    # response.headers["x-xss-protection"] = "1; mode=block"

# @bp_v1.exception(NotFound)
# async def ignore_404s(request, exception):
#     print("bp_middleware --> 404")
#     return text("Yep, I totally found the page: {}".format(request.url))

'''=========================listener==============================================='''
async def db_setup():
    print("mysql start successfully")

@bp_v1.listener('before_server_start')
async def setup_db(app, loop):
    print('before_server_start')
    app.db = await db_setup()

@bp_v1.listener('after_server_start')
async def notify_server_started(app, loop):
    print('after_server_start')

@bp_v1.listener('before_server_stop')
async def notify_server_stopping(app, loop):
    print('before_server_stop')

@bp_v1.listener('after_server_stop')
async def close_db(app, loop):
    print('after_server_stop')
    # await app.db.close()

'''========================================================================'''
from app.api import test            #别再不小心删了哥
