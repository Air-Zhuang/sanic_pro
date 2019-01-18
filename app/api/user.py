from sanic.response import json
from app.lib.token_auth import authorized
from app.models.user import User
from . import bp_v1


# @api.route('/<int:uid>',methods=['GET'])
# @auth.login_required
# def super_get_user(uid):
#     user=User.query.filter_by(id=uid).first_or_404()
#     return jsonify(user)

@bp_v1.route('/user/<id>',methods=['GET'])
@authorized()
async def get_user(request,id):
    user=User(request=request)
    result=await user.select_information("id",id)
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

