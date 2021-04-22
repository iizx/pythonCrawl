# -*- coding:utf8 -*
import requests
import json

start_url = 'https://i.news.qq.com/trpc.qqnews_web.kv_srv.kv_srv_http_proxy/list'
# 'https://i.news.qq.com/trpc.qqnews_web.kv_srv.kv_srv_http_proxy/list?sub_srv_id=ent&srv_id=pc&offset=0&limit=20&strategy=1&ext=%7B%22pool%22%3A%5B%22hot%22%5D%2C%22is_filter%22%3A2%2C%22check_type%22%3Atrue%7D'
#  https://i.news.qq.com/trpc.qqnews_web.kv_srv.kv_srv_http_proxy/list?sub_srv_id=ent&srv_id=pc&offset=0&limit=20&strategy=1&ext={%22pool%22:[%22hot%22],%22is_filter%22:2,%22check_type%22:true}
def get_info(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36',
        'Referer': 'https://new.qq.com/'
    }
    params = {
        'sub_srv_id': 'ent',
        'srv_id': 'pc',
        'offset': 0,
        'limit': 20,
        'strategy': 1,
        'ext': r'{"pool":["hot"],"is_filter":2,"check_type":true}'
    }
    page_source = requests.get(url,headers=headers,params=params)
    infos = json.loads(page_source.text)
    # print(infos)
    for item in infos['data']['list']:
        print(item['title'])

get_info(start_url)