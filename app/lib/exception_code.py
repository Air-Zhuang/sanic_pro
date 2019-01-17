from sanic.response import HTTPResponse
from ujson import dumps as json_dumps

def ServerError():
    return HTTPResponse(
        json_dumps({ "code": 500, "message": "大哥，你500了" }),
        headers=None,
        status=500,
        content_type="application/json",
    )

def Success(request):
    code=201            #操作成功的返回，不要被继承APIException迷惑，这里会返回201
    msg='ok'
    error_code = 0      #自定义成功信息
    return HTTPResponse(
        json_dumps({"error_code" : 0,"message": "ok","request":request.method+" "+request.path}),
        headers=None,
        status=201,
        content_type="application/json",
    )