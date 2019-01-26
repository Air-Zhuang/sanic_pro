from sanic import Sanic
from sanic.response import json,text
from sanic import Blueprint
from sanic_jwt import Initialize

app = Sanic()

async def authenticate(request):
    # return dict(user_id='some_id')
    return {'user_id':'some_id'}

# Initialize(app, authenticate=authenticate,path_to_authenticate='/my_authenticate',
#     path_to_retrieve_user='/my_retrieve_user',
#     path_to_verify='/my_verify',
#     path_to_refresh='/my_refresh',)
Initialize(app, authenticate=authenticate)

@app.get('/',)
async def handler(request):
    return text('OK')

@app.get('/me',)
async def extend_retrieve_user(request, user=None, payload=None):
    return json({"user":user})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000,debug=True)