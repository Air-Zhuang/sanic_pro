import requests
from scrapy.selector import Selector
from contextlib import contextmanager

def list_strip(l):
    return list(map(str.strip,l))

@contextmanager
def auto_except():
    try:
        yield
    except Exception as e:
        pass

def get_goods_detail(url):
    data={
        "category_list":None,
        "price":None,
        "rank_list":None,
        "reviews":None,
        "star":None,
        "star_distribute_list":None,
    }
    '''==================阿布云=================================='''
    # 代理服务器
    proxyHost = "proxy.abuyun.com"
    proxyPort = "9010"

    # 代理隧道验证信息
    proxyUser = "H19L33N1C59OU8YP"
    proxyPass = "B95DABFFC890CBD7"

    proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
        "host": proxyHost,
        "port": proxyPort,
        "user": proxyUser,
        "pass": proxyPass,
    }
    print(proxyMeta)
    proxies = {
        "http": proxyMeta,
        "https": proxyMeta,
    }
    '''=========================================================='''

    headers = {
            # "Proxy-Switch-Ip": "yes",
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36"
        }

    try:
        res=requests.get(url=url,proxies=proxies,headers=headers)
        response=Selector(text=res.text)
    except Exception as e:
        res = requests.get(url=url, headers=headers)
        response = Selector(text=res.text)

    '''=====================商品分类====================='''
    with auto_except():
        category_list=list_strip(response.css("#wayfinding-breadcrumbs_feature_div .a-unordered-list li a::text").extract())
    if not category_list:
        with auto_except():
            category_list=response.css("#SalesRank a::text").extract_first().replace("See Top 100 in ","")
    data["category_list"]=category_list if category_list else None

    '''=====================商品价格====================='''
    with auto_except():
        price=response.css("#priceblock_ourprice::text").extract()
    if not price:
        with auto_except():
            price=response.css("#priceblock_dealprice::text").extract()
    if not price:
        with auto_except():
            price=response.css("#priceblock_pospromoprice::text").extract()
    data["price"] = price if price else None


    '''=====================商品排行====================='''
    rank_list=[]
    with auto_except():
        rank_list.append(response.xpath('//li[@id="SalesRank"]/text()').extract()[1].strip().replace("(",""))
        l=response.css("#SalesRank .zg_hrsr li")
        for i in l:
            rank_list.append(i.css(".zg_hrsr_rank::text").extract_first()+" in "+">".join(i.css(".zg_hrsr_ladder a::text").extract()))
        data["rank_list"] = rank_list if rank_list else None
    if not rank_list:
        l=response.css("#productDetails_detailBullets_sections1 tr")
        for i in l:
            if "Best Sellers Rank" in i.css("th::text").extract_first():
                l2=i.css("td>span span")
                for j in l2:
                    rank_list.append("".join(j.css("::text").extract()))
        data["rank_list"] = rank_list if rank_list else None


    '''=====================评论数====================='''
    reviews=response.css("#dp-summary-see-all-reviews h2::text").extract()
    data["reviews"] = reviews if reviews else None

    '''=====================评分====================='''
    star=response.css(".arp-rating-out-of-text::text").extract()
    data["star"] = star if star else None

    '''=====================评分分布====================='''
    star_distribute_list=[]
    star_distribute=response.css("#histogramTable tr")
    for i in star_distribute:
        try:
            star_distribute_list.append(i.css("td a::text").extract()[-1])
        except Exception as e:
            print("0%")
    data["star_distribute_list"] = star_distribute_list if star_distribute_list else None

    return data
