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
            sql = 'SELECT * FROM `user` WHERE email="{}" AND status=1;'. \
                format(param)
            async with self.request.app.db.acquire() as conn:
                async with conn.cursor() as cur:
                    found = await cur.execute(sql)
                    if found == 1:
                        (create_time, status, id, email, nickname, auth, password) = await cur.fetchone()
                        return (create_time, status, id, email, nickname, auth, password)
            return None
        if by=="id":
            sql = 'SELECT * FROM `user` WHERE id={} AND status=1;'. \
                format(param)
            async with self.request.app.db.acquire() as conn:
                async with conn.cursor() as cur:
                    found = await cur.execute(sql)
                    if found == 1:
                        (create_time, status, id, email, nickname, auth, password) = await cur.fetchone()
                        return {"auth":auth,"email":email,"id":id,"nickname":nickname}
            return None

    async def delete_user_by_id(self,param):        #软删除用户
        sql = 'UPDATE user SET status=0 WHERE id={} AND status=1;'. \
            format(param)
        async with self.request.app.db.acquire() as conn:
            async with conn.cursor() as cur:
                found = await cur.execute(sql)
                return found


    async def verify(self,password):
        result=await self.select_information("email",self.account)
        if result:
            verfy = await self.check_secret(result[6], password)
            if verfy:
                scope = 'AdminScope' if result[5] == 2 else 'UserScope'
                return {'uid':result[2],'scope':scope}
            else:
                return "Password Incorrect"
        else:
            return "User Not Found"