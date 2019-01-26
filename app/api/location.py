from sanic.response import json
from app.lib.exception_code import NotFound
from app.lib.location_factory import get_shortcode
from . import bp_v1

@bp_v1.route('/location/search')
async def location_search(request):
    short_code=get_shortcode(request.raw_args['q'])
    if short_code:
        return json({"result":short_code})
    return NotFound(request)
