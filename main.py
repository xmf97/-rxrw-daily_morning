from datetime import date, datetime
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random
import json


today = datetime.now()
start_date = os.environ['START_DATE']
city = os.environ['CITY']
birthday = os.environ['BIRTHDAY']

app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]

user_id = os.environ["USER_ID"]
template_id = os.environ["TEMPLATE_ID"]

def get_date():
    today_date = datetime.now().strftime('%Y-%m-%d')
    week_list = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]
    dayOfWeek = datetime.today().weekday()
    return today_date + " " + week_list[dayOfWeek]



def get_weather():
    key = '546747845e36409aa64d36372c4eb367'  # 我自己的和风天气key，你最好自己注册一个，免费的
    location = '101130107'  # 城市代码101180801
    city = '乌鲁木齐'
    address = "https://devapi.qweather.com/v7/weather/3d?"
    params = {
        'location': location,
        'key': key,
        'lang': 'zh'}
    res = requests.get(address,params)
    jsondata = res.json()['daily']
    todaydata=jsondata[0]
    return todaydata['textDay'],int(todaydata['humidity']),int(todaydata['tempMax']),int(todaydata['tempMin']),todaydata['windScaleDay']


def get_count():
  delta = today - datetime.strptime(start_date, "%Y-%m-%d")
  return delta.days

def get_birthday():
  next = datetime.strptime(str(date.today().year) + "-" + birthday, "%Y-%m-%d")
  if next < datetime.now():
    next = next.replace(year=next.year + 1)
  return (next - today).days

def get_words():
	url = 'http://open.iciba.com/dsapi/'
	r = requests.get(url)
    words =  json.loads(r.text)["note"]
  return words

def get_random_color():
  return "#%06x" % random.randint(0, 0xFFFFFF)


client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)
today_date = get_date()
wea, humidity,tempMax,tempMin,windScaleDay = get_weather()
data = {
        "date":{"value":today_date,"color":get_random_color()},
        "weather":{"value":wea,"color":get_random_color()},
        "humidity":{"value":str(humidity) + "%","color":get_random_color()},
        "tempMax":{"value":str(tempMax) + "度","color":get_random_color()},
        "tempMin":{"value":str(tempMin) + "度","color":get_random_color()},
        "windScaleDay":{"value":str(windScaleDay) + "级","color":get_random_color()},
        "love_days":{"value":get_count(),"color":get_random_color()},
        "birthday_left":{"value":get_birthday(),"color":get_random_color()},
        "words":{"value":get_words(), "color":get_random_color()}}
res = wm.send_template(user_id, template_id, data)
print(res)
