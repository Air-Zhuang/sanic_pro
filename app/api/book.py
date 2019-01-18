from sanic.response import json
from app.validators.forms import BookSearchForm
from app.lib.exception_code import ParameterException,NotFound
from app.models.book import Book
from . import bp_v1

@bp_v1.route('/book/search')
async def search(request):
    '''
    url http://localhost:5000/v1/book/search?q={}
    '''
    form = BookSearchForm(data=request.raw_args)
    if BookSearchForm(data=request.raw_args).validate():
        book=Book(request)
        q=form.q.data
        result=await book.search_by_title_or_publisher(q)
        if result:
            resp={"result":result,"flag": 1}         #返回值拼接成json格式
            return json(resp)
        return NotFound(request)
    return ParameterException(request)

@bp_v1.route('/book/<isbn>/detail')
async def detail(request,isbn):
    book = Book(request)
    result=await book.search_single_book("isbn",isbn)
    if result:
        return json(result)
    return NotFound(request)
