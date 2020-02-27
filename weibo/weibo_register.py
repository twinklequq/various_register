# -*- coding: utf-8 -*-


import base64
import time
import json
import re
import requests
import rsa
import binascii
import random
from PIL import Image


s = requests.Session()
prelogin_url = "https://login.sina.com.cn/sso/prelogin.php"
login_url = "https://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.19)"
headers = {
    'Referer': 'https://weibo.com/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36'
}
parms = {
    'entry': 'weibo',
    'callback': 'sinaSSOController.preloginCallBack',
    'su': '',
    'rsakt': 'mod',
    'checkpin': '1',
    'client': 'ssologin.js(v1.4.19)',
    '_': ''
}
user = ''
pwd = ''
su = base64.b64encode(user.encode('utf-8'))
timestamp = str(time.time() * 1000).split('.')[0]
parms['_'] = timestamp
response = s.get(url=prelogin_url, headers=headers, params=parms).text
pattern = re.compile(r'[(](.*?)[)]', re.S)
re_match = re.findall(pattern, response)[0]
prelogin_res = json.loads(re_match)
print(prelogin_res)
servertime = prelogin_res['servertime']
nonce = prelogin_res['nonce']
pcid = prelogin_res['pcid']
print("pcid:", pcid)
captcha_param = "".join([str(random.randint(0, 9)) for i in range(8)])
captha_url = 'https://login.sina.com.cn/cgi/pin.php?r=' + captcha_param + '&s=0&p=' + pcid
img = requests.get(captha_url, headers=headers).content
with open('img.jpg', 'wb') as fp:
    fp.write(img)
img = Image.open('img.jpg')
img.show()
captcha = input("输入验证码：")
rsa_pubkey = rsa.PublicKey(int(prelogin_res['pubkey'], 16), int('10001', 16))
msg = bytes("" + "\t".join([str(servertime), nonce]) + "\n" + pwd, encoding='utf-8')
encrypt_msg = rsa.encrypt(msg, rsa_pubkey)
sp = binascii.b2a_hex(encrypt_msg).decode('utf-8')
login_params = {
    'entry': 'weibo',
    'gateway': 1,
    'from': '',
    'savestate': 7,
    'qrcode_flag': 'false',
    'useticket': 1,
    'pagerefer': 'https://www.baidu.com/link?url=qGwMmTRMoce1DlDa0gZpV3WtVoZh1GGQs832cVU9fPu&wd=&eqid=ac884769000a62b6000000065dfdeda9',
    'vsnf': 1,
    'pcid': pcid,
    'door': captcha,
    'su': su,
    'service': 'miniblog',
    'servertime': '',
    'nonce': nonce,
    'pwencode': 'rsa2',
    'rsakv': prelogin_res['rsakv'],
    'sp': sp,
    'sr': '1366*768',
    'encoding': 'UTF-8',
    'prelt': '',
    'url': 'https://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack',
    'returntype': 'META'
}
servertime = str(time.time()).split('.')[0]
prelt = int(servertime) - int(servertime) - int(prelogin_res['exectime'])
login_params['prelt'] = prelt
login_params['servertime'] = servertime
login_res = s.post(url=login_url, data=login_params, headers=headers).content.decode('gbk')
redirect_pattern = re.compile(r'location\.replace\((.*?)\)', re.S)
redirect_url = re.findall(redirect_pattern, login_res)[0].replace('"', '')
print("redirect_url:", redirect_url)
crossdomain_response = s.get(url=redirect_url, headers=headers.update(
    {
    'Referer': login_url
    }
))
crossdomain_res = crossdomain_response.content.decode('gbk')
print('crossdomain_res', crossdomain_res)
crossdomain_redirect = re.findall(redirect_pattern, crossdomain_res)[0].replace("'", '')
passport = s.get(url=crossdomain_redirect, headers=headers.update(
    {
        'Referer': redirect_url
    }
))
passport_response = passport.content.decode('gbk')
cookies = passport.cookies
cookie_data = {}
for k, v in cookies.items():
    cookie_data[k] = v
print(cookie_data)
# s.get(url='https://weibo.com/nguide/interest', headers=headers)
# s.get(url='https://weibo.com/nguide/interests', headers=headers)
pattern_userid = re.compile(r'"uniqueid":"(.*?)"')
userid = re.findall(pattern_userid, passport_response)
if userid:
    weibo_url = "https://weibo.com/u/{}/home".format(userid)
    weibo_response = s.get(url=weibo_url, headers=headers.update({
        'Referer': 'https://weibo.com/'
    }))
    print(weibo_response.content.decode('utf-8'))
    cookies = weibo_response.cookies
    cookie_data = {}
    for k, v in cookies.items():
        cookie_data[k] = v
    print(cookie_data)
else:
    print("nothing found")

