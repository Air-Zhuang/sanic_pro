from sanic.response import json, text, redirect

from . import bp


@bp.route('/')
async def test(request):
    return json({'hello': 'world'})

'''=========================json==============================================='''
@bp.route("/json")
async def post_json(request):
    '''
    body:{"a":1,"b":2}
    {"received":true,"message":{"a":1,"b":2}}
    '''
    return json({ "received": True, "message": request.json })

@bp.route("/query_string")
async def query_string(request):
    '''
    /query_string?a=1&b=2
    {"parsed":true,"args":{"a":["1"],"b":["2"]},"url":"http:\/\/47.101.59.238:8000\/query_string?a=1&b=2","query_string":"a=1&b=2"}
    '''
    return json({ "parsed": True, "args": request.args, "url": request.url, "query_string": request.query_string })

@bp.route("/form")
async def post_json(request):
    '''
    a=1
    b=2
    {"received":true,"form_data":{"a":["1"],"b":["2"]},"test":null}
    '''
    return json({ "received": True, "form_data": request.form, "test": request.form.get('test') })

'''=========================post==============================================='''
@bp.route("/users", methods=["POST",])
async def create_user(request):
    return text("You are trying to create a user with the following POST: %s" % request.body)

'''=========================url_for==============================================='''

@bp.route('/urlfor')
async def index(request):
    # generate a URL for the endpoint `post_handler`
    url = request.app.url_for('bp.post_handler', post_id=5, arg_one='one', arg_two='two')
    # the URL is `/posts/5`, redirect to it
    return redirect(url)

@bp.route('/posts/<post_id>')
async def post_handler(request, post_id):
    return text('Post - '+str(post_id)+'      url - '+request.url)


