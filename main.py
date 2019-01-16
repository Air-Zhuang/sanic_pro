from sanic import Sanic
from sanic.response import json

from app.config import local_config


app = Sanic()
app.config.from_object(local_config)

@app.route('/')
async def test(request):
    return json({'hello': 'world'})

@app.route("/json")
def post_json(request):
    '''
    body:{"a":1,"b":2}
    {"received":true,"message":{"a":1,"b":2}}
    '''
    return json({ "received": True, "message": request.json })

@app.route("/query_string")
def query_string(request):
    '''
    /query_string?a=1&b=2
    {"parsed":true,"args":{"a":["1"],"b":["2"]},"url":"http:\/\/47.101.59.238:8000\/query_string?a=1&b=2","query_string":"a=1&b=2"}
    '''
    return json({ "parsed": True, "args": request.args, "url": request.url, "query_string": request.query_string })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=app.config['DEBUG'])