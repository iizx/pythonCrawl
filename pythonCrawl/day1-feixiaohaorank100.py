# -*- coding:utf8 -*
import requests
from lxml import etree
import json
url = 'https://www.feixiaohao.com/'
page_source = requests.get(url)
page_content = etree.HTML(page_source.text)
title = ''.join(page_content.xpath("//div[@class='ivu-table-header']/table/thead/tr//text()"))
print(title)
info_usrl = 'https://dncapi.bqrank.net/api/coin/web-coinrank?page=1&type=-1&pagesize=100&webp=1'
info_sourse = requests.get(info_usrl).text
infos = json.loads(info_sourse)
# print(infos['data'])
result = []
for item in infos['data']:##   币种  流通市值(¥)   全球指数(¥)   24H额(¥)   流通数量   24H换手   24H涨幅   7天指数趋势
    result.append(str(item['rank']))
    result.append(item['name'])
    result.append(item['fullname'])
    result.append(str(item['market_value']/1000000000))
    result.append(str(item['current_price']/10000))
    result.append(str(item['vol']/1000000000))
    result.append(str(item['supply']/10000))
    result.append(str(item['turnoverrate']))
    result.append(str(item['change_percent']))
    print(' '.join(result))
    result = []