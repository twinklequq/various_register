# -*- coding: utf-8 -*-


import requests
import time
import random
import string
import re
import base64
from PIL import Image
from fake_useragent import UserAgent


s = requests.session()
img_url = "https://kyfw.12306.cn/passport/captcha/captcha-image64"
check_url = "https://kyfw.12306.cn/passport/captcha/captcha-check"
login_url = "https://kyfw.12306.cn/passport/web/login"
userLogin_url = "https://kyfw.12306.cn/otn/login/userLogin"
index_url = "https://kyfw.12306.cn/otn/view/index.html"
jq = 'jQuery1910' + ''.join([random.choice(string.digits) for i in range(16)]) + '_'
callback_time = round(time.time() * 1000)
img_params = {
    'login_site': 'E',
    'module': 'login',
    'rand': 'sjrand',
    'callback': jq + str(callback_time),
    '_': str(callback_time + 1)
}
ua = UserAgent()
headers = {
    'User-Agent': ua.random
}
response = s.get(url=img_url, headers=headers, params=img_params)
content = response.text
pattern = re.compile('"image":"(.*?)",', re.S)
image = re.findall(pattern, content)
if image:
    image = image[0]
img = base64.b64decode(image)
with open('captcha.jpg', 'wb') as fp:
    fp.write(img)
im = Image.open('captcha.jpg')
im.show()
position = {
    '1': '36,46',
    '2': '100,46',
    '3': '184,60',
    '4': '246,60',
    '5': '40,118',
    '6': '108,115',
    '7': '194,113',
    '8': '232,106'
}
positions = input("输入目标位置(按照从上到下，从左到右的顺序排序):\n")
pos_str = ','.join([position[i] for i in list(positions)])
check_params = {
    'login_site': 'E',
    'answer': pos_str,
    'rand': 'sjrand',
    'callback': jq + str(callback_time),
    '_': str(callback_time + 2)
}
check_response = s.get(url=check_url, headers=headers, params=check_params)
user = ''
pwd = ''
login_params = {
    'username': user,
    'password': pwd,
    'appid': 'otn',
    'answer': pos_str
}
login_response = s.post(url=login_url, headers=headers, data=login_params)
redirect = s.get(url=userLogin_url, headers=headers)
index = s.get(url=index_url, headers=headers)
ticket_url = "https://kyfw.12306.cn/otn/leftTicket/init"
link_params = {
    'linktypeid': 'dc'
}
ticket_response = s.get(url=ticket_url, headers=headers, params=link_params)
query_url = "https://kyfw.12306.cn/otn/leftTicket/queryZ"
query_params = {
    'leftTicketDTO.train_date': '2020-01-17',
    'leftTicketDTO.from_station': 'NJH',
    'leftTicketDTO.to_station': 'YLH',
    'purpose_codes': 'ADULT'
}
query_response = s.get(url=query_url, headers=headers, params=query_params)
with open('shift.txt', 'w') as fp:
    fp.write(query_response.json())

