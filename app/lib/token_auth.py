from collections import namedtuple
from functools import wraps
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer,BadSignature,SignatureExpired
from app.lib.exception_code import AuthFailed,AuthFailed2

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
                return AuthFailed2(request,1007,"authorization failed")

            print(user_info)
            if isinstance(user_info,User):
                response = await f(request, *args, **kwargs)
                print("!!!!!!!!authorized")
                return response
            else:
                return AuthFailed2(request,1008,"authorization failed")
        return decorated_function
    return decorator

# @auth.verify_password
# def verify_password(token,password):
#     '''
#     header传账号密码格式:
#         key=Authorization
#         value=basic base64(Air:123456)
#     '''
#     user_info=verify_auth_token(token)
#     if not user_info:
#         return False                    #拿不到用户信息，返回验证不通过
#     else:
#         g.user=user_info                #将用户信息放在 g 变量中
#         return True

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
    # allow=is_in_scope(scope,request.endpoint)     #endpoint表示要访问的视图函数，类似于url_for
    # if not allow:
    #     raise Forbidden()
    return User(uid,ac_type,scope)