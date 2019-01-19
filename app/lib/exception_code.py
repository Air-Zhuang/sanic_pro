from sanic.handlers import ErrorHandler
from sanic.exceptions import SanicException
from sanic.response import HTTPResponse
from ujson import dumps as json_dumps


class CustomHandler(ErrorHandler):
    def default(self, request, exception):
        # Here, we have access to the exception object
        # and can do anything with it (log, send to external service, etc)

        # Some exceptions are trivial and built into Sanic (404s, etc)
        if not isinstance(exception, SanicException):
            print("!!!!!!exception:!!!!!!",exception)
            return ServerError(request)

        # Then, we must finish handling the exception by returning
        # our response to the client
        # For this we can just call the super class' default handler
        return super().default(request, exception)

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

def DeleteSuccess(request):
    return HTTPResponse(
        json_dumps({"error_code" : 0,"message": "ok","request":request.method+" "+request.path}),
        headers=None,
        status=202,
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