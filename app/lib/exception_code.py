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