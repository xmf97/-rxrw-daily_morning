from datetime import date, datetime
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random

today = datetime.now()
start_date = os.environ['START_DATE']
city = os.environ['CITY']
birthday = os.environ['BIRTHDAY']

app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]

user_id = os.environ["USER_ID"]
template_id = os.environ["TEMPLATE_ID"]


def get_weather():
    key = '546747845e36409aa64d36372c4eb367'  # 我自己的和风天气key，你最好自己注册一个，免费的
    location = '101070101'  # 城市代码
    city = '北京'
    address = "https://devapi.qweather.com/v7/weather/3d?"
    params = {
        'location': location,
        'key': key,
        'lang': 'zh'}
    res = requests.get(address,params)
    jsondata = res.json()['daily']
    todaydata=jsondata[0]
    return todaydata['textDay'],int(todaydata['tempMax'])

def get_count():
  delta = today - datetime.strptime(start_date, "%Y-%m-%d")
  return delta.days

def get_birthday():
  next = datetime.strptime(str(date.today().year) + "-" + birthday, "%Y-%m-%d")
  if next < datetime.now():
    next = next.replace(year=next.year + 1)
  return (next - today).days

def get_words():
  words =  "到喝水吃药的时间了，维生素最佳服用时间在下午三点到五点之间，可以和叶黄素同时服用，祝你天天开心，越来越美！"

  return words

def get_random_color():
  return "#%06x" % random.randint(0, 0xFFFFFF)


client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)
wea, temperature = get_weather()
data = {"weather":{"value":wea},"temperature":{"value":temperature},"love_days":{"value":get_count()},"birthday_left":{"value":get_birthday()},"words":{"value":get_words(), "color":get_random_color()}}
res = wm.send_template(user_id, template_id, data)
print(res)
