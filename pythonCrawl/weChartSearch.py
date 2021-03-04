# -*- coding:utf8 -*
# 目标：通过搜狗微信搜索接口实现公众号精准搜素及相关信息爬取

# 思路分析：
#
# 1. 首先通过搜狗主页（https://www.sogou.com），找到微信搜索接口（https://weixin.sogou.com）
# 2. 以公众号：菜鸟教程为例，找到搜狗公众号搜素链接格式（https://weixin.sogou.com/weixin?query=菜鸟教程）
# 3. 抽取公众号基本信息，并返回字典

import requests
from idna import unichr
from lxml import etree
from fake_useragent import UserAgent
import re
import json

ua = UserAgent()
headers = {
    'User-Agent': ua.random
}

def gzh_info(name):
    # 方式一：拼接链接字符串
    url = 'https://weixin.sogou.com/weixin?query={}'.format(name)
    # 请求发送
    respons = requests.get(url,headers=headers)
    # 数据解析
    s = etree.HTML(respons.text)
    # 信息提取
    item = {}
    if(s.xpath('//div[@class="text-info"]')):
        print('哎呀！！暂无该公众号')
    else:
        item['gzh_name'] = s.xpath('//*[@id="sogou_vr_11002301_box_0"]/div/div[2]/p[1]/a/em/text()')[0]
        if(item['gzh_name']!=name):
            print('哎呀！！！暂无完全匹配公众号')
        else:
            item['gzh_id'] = s.xpath('//*[@id="sogou_vr_11002301_box_0"]/div/div[2]/p[2]/label/text()')[0]
            d = s.xpath('//*[@id="sogou_vr_11002301_box_0"]/@d')[0]
            detail_url = ' https://weixin.sogou.com'+s.xpath('//*[@id="wrapper"]/script/text()')[0].split(' = "')[-1]
            r_detail = requests.get(detail_url,headers=headers)
            r_detail = json.loads(r_detail.text)['msg']
            if d in r_detail:
                item['gzh_articles_mon'] = r_detail[d].split(',')[0]
            else:
                item['gzh_articles_mon'] = 0
            item['gzh_flage'] = s.xpath('//*[@id="sogou_vr_11002301_box_0"]/dl[1]/dd/text()')[0]
            item['gzh_article_link'] = "https://weixin.sogou.com/weixin"+s.xpath('//*[@id="sogou_vr_11002301_box_0"]/dl[last()]/dd//@href')[0]
            img_url = "https:"+s.xpath('//*[@id="sogou_vr_11002301_box_0"]/div/div[1]/a/img/@src')[0]
            qrc_url = s.xpath('//*[@id="sogou_vr_11002301_box_0"]/div/div[4]/span/img[1]/@src')[0]
            gzh_img = requests.get(url=img_url, headers=headers, stream=True)
            # 存储下载图片
            # item['gzh_img'] = gzh_img.content
            # 存储链接
            item['gzh_img'] = img_url
            qrc_img = requests.get(qrc_url,headers=headers,stream=True)
            # 存储下载图片
            # item['qrc_img_url'] = qrc_img.content
            # 存储链接
            item['qrc_img_url'] = qrc_url
            print(item)
if __name__ =='__main__':
    name = input("请输入公众号名字：")
    gzh_info(name)

