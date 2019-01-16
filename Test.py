from sanic import Sanic
from sanic.response import text
from sanic_mysql import SanicMysql

app = Sanic(__name__)

app.config.update(dict(MYSQL=dict(host='127.0.0.1', port=3306,
                                  user='root', password='123456',
                                  db='ginger')))

SanicMysql(app)


@app.route("/mysql")
async def mysq(request):
    val = await request.app.mysql.query('SELECT title FROM book WHERE id=1;')
    return text(val)


app.run(host="0.0.0.0", port=8000, debug=True, workers=1)