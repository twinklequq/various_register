# -*- coding: utf-8 -*-


import base64
import random
import time
from PIL import Image
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Register:
    def __init__(self, user, pwd):
        self.url = "https://passport.bilibili.com/login?spm_id_from=333.851.b_696e7465726e6174696f6e616c486561646572.11"
        self.user = user
        self.pwd = pwd
        self.chrome_options = Options()
        self.browser = webdriver.Chrome()
        self.wait = WebDriverWait(self.browser, 10)

    def get_input_info(self):
        user = self.browser.find_element_by_css_selector("input#login-username")
        pwd = self.browser.find_element_by_css_selector("input#login-passwd")
        return user, pwd

    def get_login_button(self):
        login = self.browser.find_element_by_xpath(".//li[@class='btn-box']//a[@class='btn btn-login']")
        return login

    def get_slidebutton(self):
        slidebutton = self.wait.until(EC.presence_of_element_located((By.XPATH, ".//div[@class='geetest_slider_button']")))
        return slidebutton

    def get_pic(self):
        classname = ['geetest_canvas_bg', 'geetest_canvas_fullbg']
        picname = ['bg.png', 'fullbg.png']
        for name in classname:
            js = "var canvas = document.getElementsByClassName('" + name + "');return canvas[0].toDataURL('image/png');"
            data = self.browser.execute_script(js).split(',')[-1]
            img = base64.b64decode(data)
            with open(picname[classname.index(name)], 'wb') as fp:
                fp.write(img)

    def is_same_pixel(self, bg_load, fullbg_load, x, y):
        threshold = 40
        pixel_bg = bg_load[x, y]
        pixel_fullbg = fullbg_load[x, y]
        if abs(pixel_bg[0] - pixel_fullbg[0]) < threshold \
                and abs(pixel_bg[1] - pixel_fullbg[1]) < threshold \
                and abs(pixel_bg[2] - pixel_fullbg[2]) < threshold:
            return False
        else:
            return True

    def get_distance(self, bg_load, fullbg_load):
        width, height = Image.open("bg.png").size
        for w in range(10, width):
            for h in range(0, height):
                if self.is_same_pixel(bg_load, fullbg_load, w, h):
                    return w

    def get_tracks(self, distance):
        tracks = []
        v_0 = 0
        current = 0
        distance = distance - 9
        t = 1
        # change = distance * 4 / 5
        while current <= distance:
            a = random.randint(10, 15)
            v = v_0 + a * t
            move = v * t + a * t * t / 2
            tracks.append(round(move))
            current += move
        return tracks

    def get_trace(self, distance):
        trace = []
        distance = distance - 10
        # 设置加速距离为总距离的4/5
        faster_distance = distance * (2 / 5)
        lower_distance = distance * (4 / 5)
        # 设置初始位置、初始速度、时间间隔
        # faster_distance = distance * 3 / 4
        # t = random.randint(2, 3) / 10
        start, v0, t = 0, 0, 0.2
        while start < distance:
            if start < faster_distance:
                a = 2
            elif faster_distance < start < lower_distance:
                a = -1
            else:
                a = -2
            # 位移
            move = v0 * t + 1 / 2 * a * t * t
            # 当前时刻的速度
            v = v0 + a * t
            v0 = v
            start += move
            trace.append(round(move))
        # trace 记录了每个时间间隔移动了多少位移
        return trace

    def move_to_gap(self, tracks, slidebutton):
        ActionChains(self.browser).click_and_hold(slidebutton).perform()
        for track in tracks:
            ActionChains(self.browser).move_by_offset(xoffset=track, yoffset=0).perform()
            time.sleep(random.randint(1, 2)/100)
        time.sleep(random.randint(1, 3)/100)
        ActionChains(self.browser).release().perform()

    def start(self):
        self.browser.get(self.url)
        user, pwd = self.get_input_info()
        user.send_keys(self.user)
        pwd.send_keys(self.pwd)
        login = self.get_login_button()
        login.click()
        slide = self.get_slidebutton()
        self.get_pic()
        bg_load = Image.open("bg.png").load()
        fullbg_load = Image.open("fullbg.png").load()
        distance = self.get_distance(bg_load, fullbg_load)
        tracks = self.get_trace(distance)
        self.move_to_gap(tracks, slide)


user = ""
pwd = ""
register = Register(user, pwd)
register.start()