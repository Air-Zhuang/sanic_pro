from sanic.response import json
from app.lib.token_auth import authorized
from app.lib.exception_code import NotFound
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


# @api.route('/<int:uid>',methods=['DELETE'])
# def super_delete_user(uid):
#     pass
#
# @api.route('',methods=['DELETE'])
# @auth.login_required
# def delete_user():
#     uid=g.user.uid
#     with db.auto_commit():
#         user = User.query.filter_by(id=uid).first_or_404()
#         user.delete()
#     return DeleteSuccess()
#
# @api.route('',methods=['PUT'])
# def update_user():
#     return '/v1/user/update'

