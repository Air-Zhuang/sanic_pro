from sanic.response import HTTPResponse
from ujson import dumps as json_dumps

def ServerError():
    return HTTPResponse(
        json_dumps({ "code": 500, "message": "大哥，你500了" }),
        headers=None,
        status=500,
        content_type="application/json",
    )

