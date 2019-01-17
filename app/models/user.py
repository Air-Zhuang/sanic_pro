from werkzeug.security import generate_password_hash,check_password_hash
from datetime import datetime

class User:
    def __init__(self,request,**kwargs):
        self.request=request
        self.account=kwargs["account"]
        self.nickname=kwargs["nickname"]
        self._secret=kwargs["secret"]

    @property
    def secret(self):
        return self._secret

    async def gene_secret(self):
        self._secret = generate_password_hash(self.request.app.config['SECRET_KEY'])

    def check_secret(self):
        if not self._secret:
            return False
        return check_password_hash(self._secret,self.request.app.config['SECRET_KEY'])

    async def register_email(self):
        await self.gene_secret()
        now = int(datetime.now().timestamp())
        status = 1
        auth = 1
        sql = 'INSERT INTO `user`(create_time,status,email,nickname,auth,password) VALUES({},{},"{}","{}",{},"{}")'. \
            format(now, status, self.account, self.nickname, auth, self._secret)
        async with self.request.app.db.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(sql)

    # @staticmethod
    # def verify(email,password):
    #     user=User.query.filter_by(email=email).first_or_404()
    #     # if not user:                              #检查是否有这个用户,因为重写了get_or_404这个方法，这两行可以省略
    #     #     raise NotFound(msg='user not found')
    #     if not user.check_password(password):       #检查密码是否正确
    #         raise AuthFailed()
    #     scope='AdminScope' if user.auth==2 else 'UserScope'
    #     return {'uid':user.id,'scope':scope}