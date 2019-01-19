from sanic import Sanic
from sanic.response import json,text
from sanic import Blueprint

app = Sanic()



blueprint_v1 = Blueprint('v1', url_prefix='/api', version="v1")

@blueprint_v1.get('/get', name='get_handler')
async def handler(request):
    return text('OK')

app.blueprint(blueprint_v1)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)