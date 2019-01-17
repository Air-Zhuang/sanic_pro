from sanic import Sanic
from sanic.response import json,text
from sanic_jwt import Initialize,exceptions
from sanic_jwt import protected
from sanic import Blueprint
import sanic_auth

app = Sanic()

bp_v1 = Blueprint('bp_v1',url_prefix='/v1')

# async def authenticate(request):
#     return dict(user_id='some_id')
# sanicjwt=Initialize(bp_v1, app=app, authenticate=authenticate)


class User:
    def __init__(self, id, username, password):
        self.user_id = id
        self.username = username
        self.password = password
    def __repr__(self):
        return "User(id='{}')".format(self.user_id)
    def to_dict(self):
        return {"user_id": self.user_id, "username": self.username}
users = [User(1, "user1", "abcxyz"), User(2, "user2", "abcxyz")]
username_table = {u.username: u for u in users}
userid_table = {u.user_id: u for u in users}
@bp_v1.route('/')
async def authenticate(request, *args, **kwargs):
    username = request.json.get("username", None)
    password = request.json.get("password", None)

    if not username or not password:
        raise exceptions.AuthenticationFailed("Missing username or password.")

    user = username_table.get(username, None)
    if user is None:
        raise exceptions.AuthenticationFailed("User not found.")

    if password != user.password:
        raise exceptions.AuthenticationFailed("Password is incorrect.")

    return user
sanicjwt=Initialize(bp_v1, app=app, authenticate=authenticate)


@bp_v1.route('/protect')
@sanicjwt.protected()
async def index(request):
    return json({'hello': 'world'})


app.blueprint(bp_v1)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000,debug=True)

