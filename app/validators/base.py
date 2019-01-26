from wtforms import Form
from app.lib.exception_code import ParameterException,DeleteSuccess


class BaseForm(Form):
    def __init__(self,request):
        data=request.json
        self.request=request
        super().__init__(data=data)
    def validate_for_api(self):
        valid=super().validate()
        print("|||||||||||",valid)
        if not valid:
            return DeleteSuccess(self.request)
        # return self