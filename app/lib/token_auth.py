from collections import namedtuple
from functools import wraps
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer,BadSignature,SignatureExpired
from app.lib.exception_code import Forbidden,AuthFailed2
from app.lib.scope import is_in_scope

User=namedtuple('User',['uid','ac_type','scope'])

def authorized():
    '''
    request.token从headers的Authorization字段接收令牌-->交给verify_auth_token解析-->将解析出的用户信息放到request["user_info"]字段
    '''
    def decorator(f):
        @wraps(f)
        async def decorated_function(request, *args, **kwargs):
            if request.token:
                user_info = verify_auth_token(request,request.token)    #request.token:获取headers的Authorization字段
            else:
                return AuthFailed2(request,1007,"Can not find Authorization in headers")

            if isinstance(user_info,User):
                request["user_info"] = user_info
                response = await f(request,*args, **kwargs)
                return response
            elif user_info=="Forbidden":
                return Forbidden(request)
            else:
                return AuthFailed2(request,1008,"authorization failed")
        return decorated_function
    return decorator

def verify_auth_token(request,token):       #获取token中的信息。验证token合法性
    s = Serializer(request.app.config['SECRET_KEY'])
    try:
        data=s.loads(token)         #解密的方法
    except BadSignature:
        return AuthFailed2(request,1002,'token is invalid')
    except SignatureExpired:
        return AuthFailed2(request,1003,'token is expired')
    uid=data['uid']
    ac_type=data['type']
    scope=data['scope']
    if not request.uri_template.endswith("/"):
        request.uri_template += "/"
    allow=is_in_scope(scope,request.method+"+"+request.uri_template)     #endpoint表示要访问的视图函数，类似于url_for
    # print(request.method+"+"+request.uri_template)
    # print(allow)
    if not allow:
        return "Forbidden"
    return User(uid,ac_type,scope)