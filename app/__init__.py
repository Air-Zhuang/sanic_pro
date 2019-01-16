from sanic import Sanic
from app.config import local_config


app = Sanic(__name__)


from app.api import bp
app.blueprint(bp)

app.config.from_object(local_config)
