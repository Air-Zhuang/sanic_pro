from app.lib.exception_code import Success,ParameterException
from app.validators.forms import ClientForm,UserEmailForm
from app.models.user import User
from . import bp_v1


@bp_v1.route("/client/register",methods=['POST'])
async def create_client(request):
    '''
    http://127.0.0.1:5000/v1/client/register
    {"account":"111@qq.com","secret":"123456","type":100,"nickname":"sanic"}
    '''
    form=ClientForm(data=request.json)
    if ClientForm(data=request.json).validate():
        promise = {
            100:__register_user_by_email
        }
        await promise[form.type.data](request)
        return Success(request)
    return ParameterException(request)


async def __register_user_by_email(request):
    form=UserEmailForm(data=request.json)
    if form.validate():
        user=User(request=request,**request.json)
        await user.register_email()