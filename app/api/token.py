from sanic.response import json
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, SignatureExpired, BadSignature
from app.validators.forms import ClientForm,TokenForm
from app.lib.exception_code import ParameterException
from app.lib.exception_code import AuthFailed,AuthFailed2
from app.models.user import User
from . import bp_v1

@bp_v1.route('/token',methods=['POST'])
async def get_token(request):
    """
    生成令牌
    传入账号密码-->验证是否有这个用户-->返回id,scope-->生成令牌：将id,客户端类型,scope,过期时间,SECRET_KEY写入到令牌中-->返回给客户端这个令牌
    """
    '''
        http://localhost:5000/v1/token
        {"account":"999@qq.com","secret":"123456","type":100}
    '''
    form = ClientForm(data=request.json)
    if ClientForm(data=request.json).validate():
        user = User(request=request, **request.json)
        promise = {
            100: user.verify
        }
        identity=await promise[form.type.data](
            form.secret.data
        )
        if identity=="User Not Found":
            return AuthFailed2(request,1006,"User Not Found")  #找不到用户
        if identity=="Password Incorrect":
            return AuthFailed(request) #密码验证错误

        # 生成token令牌
        expiration = request.app.config['TOKEN_EXPIRATION']
        token = generate_auth_token(request,identity['uid'], request.json["type"], identity['scope'], expiration)
        t = {
            'token': token.decode('ascii')  # 将bytes类型字符串转化成普通字符串
        }
        return json(t,status=201)
    return ParameterException(request)


@bp_v1.route('/token/secret', methods=['POST'])
async def get_token_info(request):
    """获取令牌信息"""
    '''
    http://localhost:5000/v1/token/secret
    {"token":"eyJhbGciOiJIUzIgjb7Y"}
    '''
    form = TokenForm(data=request.json)
    if TokenForm(data=request.json).validate():
        s = Serializer(request.app.config['SECRET_KEY'])
        try:
            data = s.loads(form.token.data, return_header=True)
        except SignatureExpired:
            return AuthFailed2(request,1003,'token is expired')
        except BadSignature:
            return AuthFailed2(request,1002,'token is invalid')

        r = {
            'scope': data[0]['scope'],
            'create_at': data[1]['iat'],        #token创建时间
            'expire_in': data[1]['exp'],        #token有效期
            'uid': data[0]['uid']
        }
        return json(r)

def generate_auth_token(request,uid,ac_type,scope=None,expiration=7200):    #scope:权限作用域，expiration:过期时间
    '''生成token令牌的方法'''
    s=Serializer(request.app.config['SECRET_KEY'],expires_in=expiration)
    return s.dumps({            #调用序列化器的dumps方法写入想写入的信息。 返回一个bytes类型字符串
        'uid':uid,              #令牌中写入用户id
        'type':ac_type,   #令牌中写入客户端类型
        'scope':scope
    })