class Book:
    def __init__(self,request,id=None,title=None,author=None,binding=None,publisher=None,price=None,pages=None,pubdate=None,isbn=None,summary=None,image=None):
        self.request=request
        self.id=id
        self.title=title
        self.author=author
        self.binding=binding
        self.publisher=publisher
        self.price=price
        self.pages=pages
        self.pubdate=pubdate
        self.isbn=isbn
        self.summary=summary
        self.image=image

    @staticmethod
    def combine_result(result):     #查询结果序列化
        if len(result)>1:
            l = []
            for i in result:
                d = {}
                d["id"] = i[2]
                d["title"] = i[3]
                d["author"] = i[4]
                d["binding"] = i[5]
                d["publisher"] = i[6]
                d["price"] = i[7]
                d["pages"] = i[8]
                d["pubdate"] = i[9]
                d["isbn"] = i[10]
                d["summary"] = i[11]
                d["image"] = i[12]
                l.append(d)
            return l
        else:
            d = {}
            d["id"] = result[0][2]
            d["title"] = result[0][3]
            d["author"] = result[0][4]
            d["binding"] = result[0][5]
            d["publisher"] = result[0][6]
            d["price"] = result[0][7]
            d["pages"] = result[0][8]
            d["pubdate"] = result[0][9]
            d["isbn"] = result[0][10]
            d["summary"] = result[0][11]
            d["image"] = result[0][12]
            return d

    async def search_by_title_or_publisher(self,param):
        sql = 'SELECT * FROM book WHERE title LIKE "%{}%" or publisher LIKE "%{}%";'. \
            format(param,param)
        async with self.request.app.db.acquire() as conn:
            async with conn.cursor() as cur:
                found = await cur.execute(sql)
                if found:
                    result = await cur.fetchall()
                    result=self.combine_result(result)
                    return result
                return None

    async def search_single_book(self,type,param):
        if type=="isbn":
            sql = 'SELECT * FROM book WHERE isbn={};'. \
                format(param)
            async with self.request.app.db.acquire() as conn:
                async with conn.cursor() as cur:
                    found = await cur.execute(sql)
                    if found:
                        result = await cur.fetchall()
                        result=self.combine_result(result)
                        return result
                    return None
