#-*-coding:utf8-*-
import itchat
import datetime, os, platform,time
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import requests
from lxml import etree
from pprint import pprint
import json


def get_agent():
    import random
    user_agent_list = [
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"
        "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
    ]
    return random.choice(user_agent_list)

def timerfun(sched_time) :
    flag = 0
    while True:
        now = datetime.datetime.now()
        if now > sched_time and now < sched_time + datetime.timedelta(seconds=1) :  # 因为时间秒之后的小数部分不一定相等，要标记一个范围判断
            send_move()
            time.sleep(1)    # 每次判断间隔1s，避免多次触发事件
            flag = 1
        else :
            #print('schedual time is {0}'.format(sched_time))
            #print('now is {0}'.format(now))
            if flag == 1 :
                sched_time = sched_time + datetime.timedelta(hours=24)  # 把目标时间增加一个小时，一个小时后触发再次执行
                flag = 0

def send_move():
    # nickname = input('please input your firends\' nickname : ' )
    #   想给谁发信息，先查找到这个朋友,name后填微信备注即可,deepin测试成功
    # users = itchat.search_friends(name=nickname)
    send_info2 = winfo
    users = itchat.search_friends(name='Newt')   # 使用备注名来查找实际用户名
    #获取好友全部信息,返回一个列表,列表内是一个字典
    print(users)
    #获取`UserName`,用于发送消息
    userName = users[0]['UserName']
    send_info3 = json.dumps(winfo,ensure_ascii=False)
    send_info3=send_info3.replace(',','\n').replace('{','').replace('}', '').replace(' ',"")
    print(send_info3)
    itchat.send(send_info3,toUserName = userName)
    # for key in send_info2:
    #     itchat.send(key+send_info2[key],toUserName = userName)
    print('succeed')

class Weather:
    def __init__(self):
        self.city_name = ""
        self.city_id = ""
        self.city_dict = {}
        self.weather_info = {}

    # 爬取天气信息
    def get_weather(self):
        url1 = "http://d1.weather.com.cn/sk_2d/{}.html?_=1544842784069".format(101090101)
        # 如果User-Agent被识别出来了，就再重新随机一个UA
        while 1:
            headers = {
                "Referer": "http://www.weather.com.cn/weather1d/{}.shtml".format(101090101),
                "User-Agent": get_agent()
            }
            res1 = requests.get(url1, headers=headers)
            if not re.search('FlashVars', res1.text):
                break
        res1.encoding = "utf-8"
        js = json.loads(res1.text.lstrip('var dataSK = '))
        url2 = "http://www.weather.com.cn/weather1d/{}.shtml".format(101090101)
        # 如果User-Agent被识别出来了，就再重新随机一个UA
        while 1:
            headers = {
                "Referer": "http://www.weather.com.cn/weather1d/{}.shtml".format(101090101),
                "User-Agent": get_agent()
            }
            res2 = requests.get(url2, headers=headers)
            if not re.search('FlashVars', res2.text):
                break
        res2.encoding = "utf-8"
        s = etree.HTML(res2.text)
        info1 = s.xpath('//*[@class="li1 hot"]/p/text()')[0]  # 紫外线指数
        info2 = s.xpath('//*[@id="chuanyi"]/a/p/text()')[0]  # 穿衣指数
        info3 = s.xpath('//*[@class="li4 hot"]/p/text()')[0]  # 洗车指数
        self.weather_info = {
            "城市": js['cityname'],
            "日期": js['date'],
            "天气": js['weather'],
            "温度": js['temp'] + '℃',
            "风向": js['WD'],
            "风力等级": js['WS'],
            "相对湿度": js['SD'],
            "PM2.5": js['aqi_pm25'],
            "紫外线指数": info1,
            "穿衣指数": info2,
            "洗车指数": info3
        }
        pprint(self.weather_info)  # 更好的打印Json格式数据
        return self.weather_info

if __name__=='__main__':
    w = Weather()
    winfo = w.get_weather()
    itchat.auto_login(hotReload=True)  # 首次扫描登录后后续自动登录
    sched_time = datetime.datetime(2019,1,31,17,22,10)   #设定初次触发事件的事件点
    print('run the timer task at {0}'.format(sched_time))
    timerfun(sched_time)