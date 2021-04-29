# -*- coding:utf8 -*
import requests
import re
import math
from lxml import etree
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import time
import pymysql


headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36',
    'Referer': 'https://search.51job.com/'
}


# 获取城市编码映射
def get_citycode(headers):
    page_source = requests.get('https://js.51jobcdn.com/in/resource/js/2021/search/common.f182f3d4.js', headers=headers)
    code_str = re.findall('window.area=(.*?)},,,', page_source.text)[0]
    city_dict = {v: k for k, v in eval(code_str).items()}
    return city_dict

# 获取总页数
def get_pages(headers, city_code, keyword):
    url = 'https://search.51job.com/list/{},000000,0000,00,9,99,{},2,1.html'.format(str(city_code), keyword)
    page_source = requests.get(url=url, headers=headers)
    pages = re.findall('jobid_count":(.*),"banner_ads"', page_source.text)[0]
    return math.ceil(int(eval(pages))/50)

# 获取单页职位数并循环请求详情页
def get_page(headers, city_code, keyword, get_pages):
    for page in range(1, get_pages+1):
        url = 'https://search.51job.com/list/{},000000,0000,00,9,99,{},2,{}.html'.format(str(city_code), keyword, page)
        page_source = requests.get(url=url, headers=headers)
        print(page_source.url)
        info_dict = eval(re.findall('"engine_search_result":\[(.*)],"jobid_count":"', page_source.text)[0])
        for info in info_dict:
            info_url = info['job_href'].replace('\\', '')
            get_info(headers, info_url)

def get_info(headers, url):
    page_source = requests.get(url=url, headers=headers)
    print(page_source.url)
    page_source.encoding = 'gbk'
    html = etree.HTML(page_source.text)
    result = {}
    result['job_id'] = html.xpath('//input[@id="hidJobID"]/@value')[0] if html.xpath('//input[@id="hidJobID"]/@value') != [] else ''
    result['职位'] = html.xpath('//div[@class="cn"]/h1/text()')[0] if html.xpath('//div[@class="cn"]/h1/text()') != [] else ''
    result['薪酬'] = html.xpath('//div[@class="cn"]/strong/text()')[0] if html.xpath('//div[@class="cn"]/strong/text()') != [] else ''
    result['公司名'] = html.xpath('//div[@class="cn"]/p[1]/a[1]/text()')[0] if html.xpath('//div[@class="cn"]/p[1]/a[1]/text()') != [] else ''
    info_list = html.xpath('//div[@class="cn"]/p[2]/@title')[0].replace('\xa0', '').split('|') if html.xpath('//div[@class="cn"]/p[2]/@title') != [] else ''
    result['区域'] = info_list[0] if len(info_list) > 1 else ''
    result['经验'] = info_list[1] if len(info_list) > 2 else ''
    result['学历'] = info_list[2] if len(info_list) > 3 else ''
    result['招聘人数'] = info_list[3] if len(info_list) > 4 else ''
    result['发布时间'] = info_list[4] if len(info_list) > 5 else ''
    result['福利'] = ','.join(html.xpath('//div[@class="cn"]/div/div//text()')).strip().replace(' ', '')[1:-2] if html.xpath('//div[@class="cn"]/div/div//text()') != [] else ''
    p_list = html.xpath('//div[@class="bmsg job_msg inbox"]/p')
    word = ''
    for p in p_list:
        word = word + p.xpath('./text()')[0].replace('\xa0', '') + '\n' if p.xpath('./text()') != [] else ''
    result['任职要求'] = word
    result['职位类别'] = ','.join(html.xpath('//div[@class="bmsg job_msg inbox"]/div[1]/p[1]//text()')[1:]) if html.xpath('//div[@class="bmsg job_msg inbox"]/div[1]/p[1]//text()') != [] else ''
    result['关键字'] = ','.join(html.xpath('//div[@class="bmsg job_msg inbox"]/div[1]/p[2]//text()')[1:]) if html.xpath('//div[@class="bmsg job_msg inbox"]/div[1]/p[2]//text()') != [] else ''
    result['联系方式'] = html.xpath('//div[@class="bmsg inbox"]/p/text()')[0] if html.xpath('//div[@class="bmsg inbox"]/p/text()') != [] else ''
    result['公司信息'] = html.xpath('//div[@class="tmsg inbox"]//text()')[0].replace('\xa0', '') if html.xpath('//div[@class="tmsg inbox"]//text()') != [] else ''
    insert_db(result)


def insert_db(result):
    engine = create_engine("mysql+pymysql://root:password@localhost:3306/test?charset=utf8", echo=True)
    Base = declarative_base()
    DBsession = sessionmaker(bind=engine)
    SQLsession = DBsession()

    class myTable(Base):
        __tablename__ = '51_jobs_info'
        id = Column(Integer(), primary_key=True)
        job_id = Column(String(1000), comment="职位ID")
        job_name = Column(String(1000), comment="职位名称")
        job_pay = Column(String(1000), comment="职位薪酬")
        company_name = Column(String(1000), comment="公司名称")
        company_area = Column(String(1000), comment="公司区域")
        job_year = Column(String(1000), comment="工作经验")
        job_education = Column(String(1000), comment="职位学历")
        job_member = Column(String(1000), comment="招聘人数")
        job_time = Column(String(1000), comment="发布时间")
        company_welfare = Column(String(1000), comment="公司福利")
        job_describe = Column(Text(), comment="职位要求")
        job_type = Column(String(1000), comment="职位类别")
        job_kw = Column(String(1000), comment="关键字")
        company_num = Column(String(1000), comment="联系方式")
        company_info = Column(Text(), comment="公司信息")
        log_date = Column(String(1000), comment="记录时间")
    Base.metadata.create_all(engine)
    info = SQLsession.query(myTable).filter_by(job_id=result['job_id']).first()
    if info:
        info.job_id = result.get('job_id', '')
        info.job_name = result.get('职位', '')
        info.job_pay = result.get('薪酬', '')
        info.company_name = result.get('公司名', '')
        info.company_area = result.get('区域', '')
        info.job_year = result.get('经验', '')
        info.job_education = result.get('学历', '')
        info.job_member = result.get('招聘人数', '')
        info.job_time = result.get('发布时间', '')
        info.company_welfare = result.get('福利', '')
        info.job_describe = result.get('任职要求', '')
        info.job_type = result.get('职位类别', '')
        info.job_kw = result.get('关键字', '')
        info.company_num = result.get('联系方式', '')
        info.company_info = result.get('公司信息', '')
        info.log_date = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    else:
        inser_data = myTable(
            job_id=result.get('job_id', ''),
            job_name=result.get('职位', ''),
            job_pay=result.get('薪酬', ''),
            company_name=result.get('公司名', ''),
            company_area=result.get('区域', ''),
            job_year=result.get('经验', ''),
            job_education=result.get('学历', ''),
            job_member=result.get('招聘人数', ''),
            job_time=result.get('发布时间', ''),
            company_welfare=result.get('福利', ''),
            job_describe=result.get('任职要求', ''),
            job_type=result.get('职位类别', ''),
            job_kw=result.get('关键字', ''),
            company_num=result.get('联系方式', ''),
            company_info=result.get('公司信息', ''),
            log_date=time.strftime('%Y-%m-%d', time.localtime(time.time()))
        )
        SQLsession.add(inser_data)
    SQLsession.commit()


if __name__ == '__main__':
    city_dict = get_citycode(headers)
    page = get_pages(headers, city_dict['成都'], 'python')
    get_page(headers, city_dict['成都'], 'python', page)