from werkzeug.security import generate_password_hash,check_password_hash
from datetime import datetime

class User:
    def __init__(self,request,account=None,nickname=None,type=None,secret=None):
        self.request=request
        self.account=account
        self.nickname=nickname
        self.type=type
        self._secret=secret

    @property
    def secret(self):
        return self._secret

    async def gene_secret(self,raw):
        self._secret = generate_password_hash(raw)

    async def check_secret(self,password,raw):
        return check_password_hash(password,raw)

    async def register_email(self):
        await self.gene_secret(self._secret)
        now = int(datetime.now().timestamp())
        status = 1
        auth = 1
        sql = 'INSERT INTO `user`(create_time,status,email,nickname,auth,password) VALUES({},{},"{}","{}",{},"{}")'. \
            format(now, status, self.account, self.nickname, auth, self._secret)
        async with self.request.app.db.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(sql)

    async def select_information(self,by,param):    #根据选择的参数查询信息
        if by=="email":
            sql = 'SELECT * FROM `user` WHERE email="{}";'. \
                format(param)
            async with self.request.app.db.acquire() as conn:
                async with conn.cursor() as cur:
                    found = await cur.execute(sql)
                    if found == 1:
                        (create_time, status, id, email, nickname, auth, password) = await cur.fetchone()
                        return (create_time, status, id, email, nickname, auth, password)
            return None

    async def verify(self,password):
        result=await self.select_information("email",self.account)
        if result:
            verfy = await self.check_secret(result[6], password)
            if verfy:
                scope = 'AdminScope' if result[5] == 2 else 'UserScope'
                print({'uid':result[2],'scope':scope})
                return {'uid':result[2],'scope':scope}
            else:
                return "Password Incorrect"
        else:
            return "User Not Found"