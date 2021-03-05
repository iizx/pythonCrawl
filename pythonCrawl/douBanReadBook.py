# -*- coding:utf8 -*
# 目标：爬取豆瓣读书热门标签（https://book.douban.com/tag/?view=type&icn=index-sorttags-all）下面所有书籍，并输入excel表格
#
# 思路分析：
#
# 1. 获取标签页面所有标签
# 2. 根据标签链接进入数据页面循环爬取书籍
# 3. 根据页面返回信息抽取书籍详情构造字典
# 4. 将字典内容写入表格并保存

import requests
from lxml import etree
from fake_useragent import UserAgent
import xlwt
ua = UserAgent()
headers = {
    'User-Agent' : ua.random
}
def get_tages_link(url):
    response = requests.get(url,headers=headers)
    r = etree.HTML(response.text)
    list_divs = r.xpath('//*[@id="content"]/div/div[1]/div[2]/div')
    tags_link = {}
    for div in list_divs:
        title_tag = div.xpath('.//a[@class="tag-title-wrapper"]/@name')[0]
        list_trs = div.xpath('.//table[@class="tagCol"]/tbody/tr')
        tag_info_list = []
        for tr in list_trs:
            list_tds = tr.xpath('./td')
            for td in list_tds:
                name_link = {}
                tag_name = ''.join(td.xpath('.//text()'))
                tag_link = 'https://book.douban.com'+td.xpath('./a/@href')[0]
                name_link[tag_name] = tag_link
                tag_info_list.append(name_link)
            tags_link[title_tag] = tag_info_list
    return tags_link

def get_book_info(dict):
    wb = xlwt.Workbook()
    for k,v in dict.items():
        small_type_book = {}
        for item in v:
            book_detail = []
            response = requests.get(list(item.values())[0],headers=headers)
            r = etree.HTML(response.text)
            list_lis = r.xpath('//ul[@class="subject-list"]/li')
            for li in list_lis:
                book_name = li.xpath('./div[2]/h2/a/text()')[0].strip()
                book_info = li.xpath('./div[2]/div[1]/text()')[0].strip()
                book_socre = ''.join(''.join(li.xpath('./div[2]/div[2]//text()')).replace('\n','').split(' '))
                book_img = li.xpath('./div[1]/a/@href')[0]
                if(len(li.xpath('./div[2]/p/text()'))>0):
                    book_sub = li.xpath('./div[2]/p/text()')[0].replace('\n','')
                else:
                    book_sub = ''
                book_detail.append([book_name,book_info,book_socre,book_sub,book_img])
            small_type_book[list(item.keys())[0]] = book_detail
        writeExcel({k:small_type_book},wb)

def setStyle(bold=False):
    style = xlwt.XFStyle()
    font = xlwt.Font()
    font.bold = bold
    style.font = font
    return style

def writeExcel(dict,wb):
    st = wb.add_sheet(list(dict.keys())[0],cell_overwrite_ok=True)
    row0 = ['分类','书名','书本信息','评分','简介','图片链接']
    for i in range(0,len(row0)):
        st.write(0,i,row0[i],setStyle(True))
    index = 0
    for k,v in dict.items():
        st.write(1, 0, list(v.keys())[0], setStyle())
        for item in list(v.values())[0]:
            index = index + 1
            for i,j in enumerate(item):
                st.write(index, i+1, j, setStyle())
            print(item)
    wb.save('./doubanBooks.xlsx')



if __name__ == '__main__':
    url = 'https://book.douban.com/tag/?view=type&icn=index-sorttags-all'
    get_book_info(get_tages_link(url))