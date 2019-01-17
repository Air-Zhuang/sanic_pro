from sanic import Sanic
from app.config import local_config
import asyncio

app = Sanic(__name__)

app.config.from_object(local_config)    #导入配置文件
from app.api import bp_v1
app.blueprint(bp_v1)                    #注册蓝图
# app.static('/static', './static')     #指定静态文件地址

@app.route('/favicon.ico')
async def favicon(request):
    print("Dont have favicon.ico")

# async def notify_server_started_after_five_seconds():
#     while True:
#         await asyncio.sleep(60*60)
#         print('Server alive!')
#
# app.add_task(notify_server_started_after_five_seconds())    #指定一个任务放入loop中