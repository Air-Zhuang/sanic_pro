from functools import wraps

from sanic.exceptions import ServerError, abort, NotFound
from sanic.response import json, text, redirect
from sanic.views import HTTPMethodView

from . import bp_v1

def authorized():       #验证权限的装饰器
    def decorator(f):
        @wraps(f)
        async def decorated_function(request, *args, **kwargs):
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

'''=========================hello world==============================================='''
@bp_v1.route('/')
@authorized()
async def test(request):
    return json({'hello': 'world'})

'''=========================json==============================================='''
@bp_v1.route("/json")
async def post_json(request):
    '''
    body:{"a":1,"b":2}
    {"received":true,"message":{"a":1,"b":2}}
    '''
    return json({ "received": True, "message": request.json })

@bp_v1.route("/query_string")
async def query_string(request):
    '''
    /query_string?a=1&b=2
    {"parsed":true,"args":{"a":["1"],"b":["2"]},"url":"http:\/\/47.101.59.238:8000\/query_string?a=1&b=2","query_string":"a=1&b=2"}
    '''
    return json({ "parsed": True, "args": request.args, "url": request.url, "query_string": request.query_string })

@bp_v1.route("/form")
async def post_json(request):
    '''
    a=1
    b=2
    {"received":true,"form_data":{"a":["1"],"b":["2"]},"test":null}
    '''
    return json({ "received": True, "form_data": request.form, "test": request.form.get('test') })

'''=========================post==============================================='''
@bp_v1.route("/users", methods=["POST",])
async def create_user(request):
    return text("You are trying to create a user with the following POST: %s" % request.body)

'''=========================url_for==============================================='''
@bp_v1.route('/urlfor')
async def index(request):
    # generate a URL for the endpoint `post_handler`
    url = request.app.url_for('bp_v1.post_handler', post_id=5, arg_one='one', arg_two='two')
    # the URL is `/posts/5`, redirect to it
    return redirect(url)

@bp_v1.route('/posts/<post_id>')
async def post_handler(request, post_id):
    return text('Post - '+str(post_id)+'      url - '+request.url)

'''=========================error-code==============================================='''
@bp_v1.route('/error_500')
async def i_am_ready_to_die(request):
    raise ServerError("Something bad happened", status_code=500)

@bp_v1.route('/error_401')
async def no_no(request):     #自定义抛出异常
        abort(401)
        # this won't happen
        text("OK")

# @bp_v1.exception(NotFound)   #将404做重定向处理
# async def handle_404_redirect(request, exception):
#     uri = request.app.url_for('bp_v1.test')
#     return redirect(uri)

'''=========================HTTPMethodView==============================================='''
class SimpleView(HTTPMethodView):
    # decorators = [authorized()]    #这里的装饰器会对每个方法附加装饰器

    @authorized()                   #这里可以单个加装饰器
    async def get(self, request, name):
      return text('I am get method+'+name)

    @authorized()
    async def post(self, request, name):
      return text('I am post method+'+name)

    async def put(self, request, name):
      return text('I am put method+'+name)

    async def patch(self, request, name):
      return text('I am patch method+'+name)

    async def delete(self, request, name):
      return text('I am delete method+'+name)

bp_v1.add_route(SimpleView.as_view(), '/methodview/<name>')

@bp_v1.route('/view_urlfor')
async def view_urlfor(request):       #url_for调用视图
    url = request.app.url_for('bp_v1.SimpleView', name="clannad")
    return redirect(url)

@bp_v1.route("/mysql")
async def mysq(request):
    val = await request.app.mysql.query('SELECT title FROM book WHERE id=1;')
    return text(val)