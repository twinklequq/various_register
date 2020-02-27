# -*- coding: utf-8 -*-


import requests
from PIL import Image
from requests.cookies import RequestsCookieJar
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class WB:
    def __init__(self, user, pwd):
        self.user = user,
        self.pwd = pwd
        self.options = Options()
        self.options.add_argument('--disable-gpu')
        self.options.add_experimental_option('excludeSwitches', ['enable-automation'])
        self.browser = webdriver.Chrome(options=self.options)
        self.wait = WebDriverWait(self.browser, 10)

    def get_input(self):
        user = self.wait.until(EC.presence_of_element_located((By.ID, 'loginname')))
        pwd = self.wait.until(EC.presence_of_element_located((By.NAME, 'password')))
        return user, pwd

    def get_img(self):
        img = self.wait.until(EC.presence_of_element_located((By.XPATH, '//img[@action-type="btn_change_verifycode"]')))
        img_url = img.get_attribute('src')
        return img_url

    def show_img(self):
        img_url = self.get_img()
        headers = {
            'Referer': 'https://weibo.com/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36'
        }
        img_data = requests.get(url=img_url, headers=headers).content
        with open('captcha.jpg', 'wb') as fp:
            fp.write(img_data)
        img_open = Image.open('captcha.jpg')
        img_open.show()

    def get_captcha_input(self):
        captcha = self.browser.find_element_by_name('verifycode')
        return captcha

    def login_button(self):
        login = self.browser.find_element_by_class_name('W_btn_a')
        return login

    def start(self):
        url = "https://weibo.com"
        self.browser.get(url)
        user, pwd = self.get_input()
        user.send_keys(self.user)
        pwd.send_keys(self.pwd)
        login = self.login_button()
        img_url = self.get_img()
        while img_url == 'about:blank':
            login.click()
            img_url = self.get_img()
        self.show_img()
        captcha_input = input('请输入验证码：')
        self.get_captcha_input().send_keys(captcha_input)
        login.click()
        cookies = self.browser.get_cookies()
        return cookies


user = ''
pwd = ''
wb = WB(user, pwd)
cookies = wb.start()

