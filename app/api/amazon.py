from sanic.response import json
from app.lib.exception_code import NotFound
from app.lib.amazon_detail import get_goods_detail
from . import bp_v1

@bp_v1.route('/amazon/detail')
async def amazon_get_detail(request):
    url=request.raw_args['url']
    if url:
        data=get_goods_detail(url)
        return json({"result":data})
    return NotFound(request)
