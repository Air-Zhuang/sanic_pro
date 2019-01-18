from sanic.response import json
from app.lib.token_auth import authorized
from app.lib.exception_code import NotFound,DeleteSuccess
from app.models.user import User
from . import bp_v1


@bp_v1.route('/user/<uid>',methods=['GET'])
@authorized()
async def super_get_user(request,uid):
    user = User(request=request)
    result = await user.select_information("id", uid)
    if result:
        return json(result)
    return NotFound(request)

@bp_v1.route('/user',methods=['GET'])
@authorized()
async def get_user(request):
    user=User(request=request)
    result=await user.select_information("id",request.headers["user_info"].uid) #装饰器将解析出的用户信息放在headers的user_info字段
    return json(result)


@bp_v1.route('/user/<uid>',methods=['DELETE'])
@authorized()
async def super_delete_user(request,uid):
    user = User(request=request)
    result = await user.delete_user_by_id(uid)
    if result:
        return DeleteSuccess(request)
    return NotFound(request)

@bp_v1.route('/user',methods=['DELETE'])
@authorized()
async def delete_user(request):
    user = User(request=request)
    result = await user.delete_user_by_id(request.headers["user_info"].uid)
    if result:
        return DeleteSuccess(request)
    return NotFound(request)

