# -*- coding:utf8 -*
import requests
from lxml import etree
start_url = 'https://weibo.com/a/hot/realtime'
def get_info(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) \
        Chrome/88.0.4324.96 Safari/537.36',
        'Cookie': 'SUB=_2AkMX2KQRf8NxqwJRmPoVxW_gb4l_zgrEieKhhFXKJRMxHRl-yT9kqnwCtRB6PFiK_mKNJ4JprWAKE-sooTaq-\
        iu7opHw; SUBP=0033WrSXqPxfM72-Ws9jqgMF55529P9D9WFaZWMfXh-feX4i4_hcj0oP; login_sid_t=133cf00fb4bf9914b12\
        9bb7a1e9e992a; cross_origin_proto=SSL; _s_tentry=passport.weibo.com; wb_view_log=1440*9002; Apache=8617\
        255334293.783.1619274537984; SINAGLOBAL=8617255334293.783.1619274537984; ULV=1619274537990:1:1:1:8617255\
        334293.783.1619274537984:',
        'Referer': 'https://weibo.com/'
    }
    page_source = requests.get(start_url, headers=headers)
    # print(page_source.text)
    html = etree.HTML(page_source.text)
    UG_lists = html.xpath('//div[@id = "PCD_pictext_i_v5"]/div/div/div')
    for item in UG_lists:
        print(item.xpath('./div/div[@class="list_des"]/h3/a/text()')[0])
if __name__ == '__main__':
    get_info('start_url')
