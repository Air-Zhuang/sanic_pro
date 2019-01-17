from sanic import Sanic
from sanic.response import json,text

app = Sanic()

@app.route('/')
async def test(request):
    # return json({'hello': 'world'})
    return text(request.method+request.path)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000,debug=True)