from functools import wraps

from sanic import Sanic
from sanic.response import json

app = Sanic()

def authorized():       #验证权限的装饰器
    def decorator(f):
        @wraps(f)
        async def decorated_function(request, *args, **kwargs):
            print(request.headers["auth"])
            print(request.headers["auth2"])
            # is_authorized = check_request_for_authorization_status(request)
            is_authorized = True

            if is_authorized:
                response = await f(request, *args, **kwargs)
                print("!!!!!!!!authorized")
                return response
            else:
                return json({'status': 'not_authorized'}, 403)
        return decorated_function
    return decorator


@app.route("/")
@authorized()
async def test(request):
    return json({"hello": "world"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000,debug=True)