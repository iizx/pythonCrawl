# -*- coding:utf8 -*
import requests
import re
import json

start_url = 'https://api.bilibili.com/x/credit/blocked/list?jsonp=jsonp&otype=0&pn=1&ps=20&callback=__jp0'
# https://api.bilibili.com/x/credit/publish/list?jsonp=jsonp&tp=0&pn=1&ps=4&callback=__jp1
# https://api.bilibili.com/x/credit/blocked/list?jsonp=jsonp&btype=&otype=0&pn=2&ps=20&callback=__jsonp__5

def get_info(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 \
        (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36',
        'Referer': 'https://www.bilibili.com/'
    }
    page_source = requests.get(url, headers=headers)
    info = re.findall(r'\((.*)\)', page_source.text)[0]
    html = json.loads(info)
    for item in html['data']:
        username = item['uname']
        reason = item['punishTitle']
        days = item['blockedDays']
        content = item['originContentModify'].replace('<br/>', '').replace('<p>', '').replace('</p>', '')
        print('用户:{},因{}被处以{}天封禁,详见：{}'.format(username, reason, days, content))

if __name__ == '__main__':
    get_info(start_url)