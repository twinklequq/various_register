# -*- coding: utf-8 -*-


from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class taobao:
    def __init__(self, user, pwd):
        self.user = user
        self.pwd = pwd
        self.url = "https://login.taobao.com/"
        self.chrome_options = Options()
        self.chrome_options.add_argument('--disable-gpu')
        self.chrome_options.add_argument('--no-sandbox')
        self.chrome_options.add_argument('--proxy-server=http://127.0.0.1:8080')
        self.chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
        self.browser = webdriver.Chrome(options=self.chrome_options)
        self.wait = WebDriverWait(self.browser, 10)

    def switch_mode(self):
        password_mode = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.qrcode-login > .login-links > .forget-pwd')))
        return password_mode

    def get_input_info(self):
        user = self.browser.find_element_by_name("TPL_username")
        pwd = self.browser.find_element_by_name("TPL_password")
        return user, pwd

    def get_login_button(self):
        login = WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.ID, "J_SubmitStatic")))
        return login

    def login(self):
        self.browser.get(self.url)
        mode = self.switch_mode()
        mode.click()
        user, pwd = self.get_input_info()
        user.send_keys(self.user)
        pwd.send_keys(self.pwd)
        login = self.get_login_button()
        login.click()


user = ""
pwd = ""
tb = taobao(user, pwd)
tb.login()
