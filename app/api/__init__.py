from sanic import Blueprint
from sanic.exceptions import NotFound
from sanic.response import text
import aiomysql
from functools import partial

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
    print("bp_middleware --> response")
    # response.headers["Server"] = "Fake-Server"        #中间件可以修改请求
    # response.headers["x-xss-protection"] = "1; mode=block"

# @bp_v1.exception(NotFound)
# async def ignore_404s(request, exception):
#     print("bp_middleware --> 404")
#     return text("Yep, I totally found the page: {}".format(request.url))

'''=========================listener==============================================='''
async def db_setup(app, loop):
    pool = await aiomysql.create_pool(**app.config['MYSQL'],loop=loop)
    print("mysql start successfully")       #初始化aiomysql
    return pool

async def db_query(pool,sqlstr,args=None):  #自己封装的查询方法
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            final_str = cur.mogrify(sqlstr, args)
            await cur.execute(final_str)
            value = await cur.fetchall()
            return value

@bp_v1.listener('before_server_start')
async def setup_db(app, loop):
    app.db = await db_setup(app, loop)
    app.db.query = partial(db_query,app.db)

@bp_v1.listener('after_server_stop')
async def close_db(app, loop):
    app.db.close()
    await app.db.wait_closed()
    print("mysql close successfully")

'''========================================================================'''
from app.api import test            #别再不小心删了,哥~~
from app.api import client
from app.api import token
from app.api import book
from app.api import user