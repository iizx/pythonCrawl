# 爬虫练习第一天：requests库练习，目标网站https://tuchong.com,获取返回信息
import requests
# 请求发送
#     get
r = requests.get("https://tuchong.com")
    # post
r2 = requests.post('https://tuchong.com')
# 请求传参，以字典形式替代传统参数输入方式
params = {
    'term' : '中国'
}
r3 = requests.get('https://tuchong.com',params=params)
# 观察返回值
# r.text,自动解码返回内容
# r.encoding,查看返回值编码方式
# r.url,查看请求连接
# r.content,以字节方式访问请求数据
print(r3.url)
