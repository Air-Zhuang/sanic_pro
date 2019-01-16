from sanic import Sanic
from sanic_mysql import SanicMysql
from app.config import local_config
import asyncio

app = Sanic(__name__)

app.config.update(dict(MYSQL=dict(host='127.0.0.1', port=3306,
                           user='root', password='123456',
                           db='ginger')))
SanicMysql(app)

from app.api import bp_v1
app.blueprint(bp_v1)           #注册蓝图

# app.static('/static', './static')     #指定静态文件地址
app.config.from_object(local_config)    #导入配置文件

# async def notify_server_started_after_five_seconds():
#     while True:
#         await asyncio.sleep(60*60)
#         print('Server alive!')
#
# app.add_task(notify_server_started_after_five_seconds())    #指定一个任务放入loop中