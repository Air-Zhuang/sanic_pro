from sanic import Sanic
from sanic.response import json,text
from sanic_jwt import Initialize,exceptions
from sanic_jwt import protected
from sanic import Blueprint
import sanic_auth

app = Sanic()

bp_v1 = Blueprint('bp_v1',url_prefix='/v1')

async def authenticate(request):
    return dict(user_id='some_id')
sanicjwt=Initialize(bp_v1, app=app, authenticate=authenticate)


@bp_v1.route('/protect')
@sanicjwt.protected()
async def index(request):
    return json({'hello': 'world'})


app.blueprint(bp_v1)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000,debug=True)

