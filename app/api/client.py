from sanic.response import json, text, redirect
from app.lib.exception_code import Success
from . import bp_v1


@bp_v1.route("/client/register",methods=['POST'])
async def create_client(request):
    '''
    http://127.0.0.1:5000/v1/client/register
    {"account":"111@qq.com","secret":"123456","type":100,"nickname":"sanic"}
    '''
    return Success(request)
    # form=ClientForm().validate_for_api()                #已经在BaseForm重写了__init__方法，这里不需要传入表单信息了。如果传过来的是json,要用data=data。使用自己重写的validate方法
    # promise={                                           #用字典的形式处理不同客户端的处理方式
    #     ClientTypeEnum.USER_EMAIL:__register_user_by_email
    # }
    # promise[form.type.data]()
    # return Success()                                    #使用return HTTPException

# async def __register_user_by_email():
#     form=UserEmailForm().validate_for_api()             #已经在BaseForm重写了__init__方法，这里不需要传入表单信息了。如果传过来的是json,要用data=data
#     User.register_by_email(form.nickname.data,form.account.data,form.secret.data)