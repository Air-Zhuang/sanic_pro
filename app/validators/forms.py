from wtforms import Form
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired, length, Email, Regexp


class ClientForm(Form):
    account=StringField(validators=[DataRequired(message='不允许为空'),length(min=5,max=32)])       #账号
    secret=StringField()                                                        #密码
    type=IntegerField(validators=[DataRequired()])                              #客户端类型

    # def validate_type(self,value):
    #     try:
    #         client=ClientTypeEnum(value.data)                                   #判断是否能将数字类型转换成枚举类型
    #     except ValueError as e:
    #         raise e                                                             #这里有异常，WTForm不会抛出，而会把异常记录在errors属性中
    #     self.type.data=client                                                   #将type赋值为枚举类型

class UserEmailForm(Form):
    account = StringField(validators=[Email(message='invalidate email')])
    secret = StringField(validators=[DataRequired(),Regexp(r'^[A-Za-z0-9_*&$#@]{6,22}$')])
    nickname = StringField(validators=[DataRequired(),length(min=2, max=22)])

    # def validate_account(self, value):
    #     if User.query.filter_by(email=value.data).first():
    #         raise ValidationError()     #抛出WTForm异常

class BookSearchForm(Form):
    q=StringField(validators=[DataRequired()])

class TokenForm(Form):
    token=StringField(validators=[DataRequired()])