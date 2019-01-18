from collections import namedtuple
from functools import wraps
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer,BadSignature,SignatureExpired
from app.lib.exception_code import Forbidden,AuthFailed2
from app.lib.scope import is_in_scope

User=namedtuple('User',['uid','ac_type','scope'])

'''
这里将token当做账号，密码不传的方式来传送token,password占位用。(如果实际调用，传入的key:value要经过base64加密)
verify_password接收令牌-->交给verify_auth_token解析-->将解析出的用户信息通过namedtuple存放在g变量中
'''

def authorized():       #验证权限的装饰器
    def decorator(f):
        @wraps(f)
        async def decorated_function(request, *args, **kwargs):
            if request.headers.get("Authorization",None):
                user_info = verify_auth_token(request,request.headers["Authorization"])
            else:
                return AuthFailed2(request,1007,"Can not find Authorization in headers")

            if isinstance(user_info,User):
                request.headers["user_info"] = user_info
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
    print(request.method+"+"+request.uri_template)
    print(allow)
    if not allow:
        return "Forbidden"
    return User(uid,ac_type,scope)