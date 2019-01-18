from sanic.response import HTTPResponse
from ujson import dumps as json_dumps

def ServerError(request):
    return HTTPResponse(
        json_dumps({"error_code" : 999,"message": "sorry, we made a mistake!","request":request.method+" "+request.path}),
        headers=None,
        status=500,
        content_type="application/json",
    )

def Success(request):
    return HTTPResponse(
        json_dumps({"error_code" : 0,"message": "ok","request":request.method+" "+request.path}),
        headers=None,
        status=201,
        content_type="application/json",
    )

def AuthFailed(request):
    return HTTPResponse(
        json_dumps({"error_code": 1005, "message": "authorization failed", "request": request.method + " " + request.path}),
        headers=None,
        status=401, #禁止访问
        content_type="application/json",
    )

def AuthFailed2(request,error_code,message):
    return HTTPResponse(
        json_dumps({"error_code": error_code, "message": message, "request": request.method + " " + request.path}),
        headers=None,
        status=401,
        content_type="application/json",
    )

def ParameterException(request):
    return HTTPResponse(
        json_dumps(
            {"error_code": 1000, "message": "invalid parameter", "request": request.method + " " + request.path}),
        headers=None,
        status=400,
        content_type="application/json",
    )

def NotFound(request):
    return HTTPResponse(
        json_dumps(
            {"error_code": 1001, "message": "The resource are not_found !", "request": request.method + " " + request.path}),
        headers=None,
        status=404,
        content_type="application/json",
    )

def Forbidden(request):
    return HTTPResponse(
        json_dumps(
            {"error_code": 1004, "message": "forbidden, not in scope","request": request.method + " " + request.path}),
        headers=None,
        status=403, #权限不够
        content_type="application/json",
    )