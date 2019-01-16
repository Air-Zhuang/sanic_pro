from sanic import Blueprint

from sanic.exceptions import NotFound
from sanic.response import text

bp = Blueprint('bp')    #给蓝图起名，慎重

@bp.middleware
async def print_on_request(request):
    print("bp_middleware")

@bp.middleware('request')
async def halt_request(request):
    print("bp_middleware --> request")

@bp.middleware('response')
async def halt_response(request, response):
    print("bp_middleware --> request")

@bp.exception(NotFound)
def ignore_404s(request, exception):
    print("bp_middleware --> 404")
    return text("Yep, I totally found the page: {}".format(request.url))

from app.api import test