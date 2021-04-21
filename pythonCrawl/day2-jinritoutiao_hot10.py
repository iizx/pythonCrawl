# -*- coding:utf8 -*
import requests
from lxml import etree
from fake_useragent import UserAgent
import json

ua = UserAgent()
headers = {
    'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36'
}
# 目标地址https://www.toutiao.com/ch/news_hot/
url = 'https://www.toutiao.com/api/pc/feed/?min_behot_time=0&refresh_count=1&category=news_hot&utm_source=toutiao&widen=1&tadrequire=true&_signature=_02B4Z6wo00d014QRV.wAAIDBtEdgaRK6VV-ENFNAAIGMprPJ4lPMIH1Fd4eLeuy1IdLW4gny7EM6WmJYT2Sa2srH9-kcXvmDpA6jtWgL2E1.I3bok7htfEhs6FmGW.49Avo9-zzSL83cRubd8a'
def get_info(url):
    page_source = requests.get(url,headers=headers)
    info = json.loads(page_source.text)
    for item in info['data']:
        print(item['title'])
    # a = u'\u91cd\u78c5\uff01\u4e8b\u5173\u53f0\u5dde200\u4f59\u4e07\u4eba\uff0c\u4e0b\u6708\u8d77\u6b63\u5f0f\u5b9e\u65bd\uff01'
    # a1 = '重磅！事关台州200余万人，下月起正式实施！'
    # b1 = a1.encode('unicode_escape')
    # b = a.encode('unicode_escape')
    # print(b.decode('unicode_escape'))
    # print(b1)
# \u91cd\u78c5\uff01\u4e8b\u5173\u53f0\u5dde200\u4f59\u4e07\u4eba\uff0c\u4e0b\u6708\u8d77\u6b63\u5f0f\u5b9e\u65bd\uff01"
if __name__ == '__main__':
    get_info(url)