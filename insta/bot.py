import os
import time
import random
import spintax
import requests
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.firefox.options import Options
# from webdriver_manager.firefox import GeckoDriverManager 

class Bot:
    def __init__(self, username, password):

        self.username = username
        self.password = password

        # options = Options()
        # options.add_argument("-headless")

        user_agent = "Mozilla/5.0 (iPhone; U; CPU iPhone OS 3_0 like Mac OS X; en-us) AppleWebKit/528.18 (KHTML, like Gecko) Version/4.0 Mobile/7A341 Safari/528.16"
        profile = webdriver.FirefoxProfile()
        profile.set_preference("general.useragent.override", user_agent)

        # self.bot = webdriver.Firefox(profile, executable_path=GM().install())
        self.bot = webdriver.Firefox(firefox_profile=profile)
        # self.bot = webdriver.Firefox(firefox_profile=profile, firefox_options=options)
        self.bot.set_window_size(500, 950)

        # with open(r'tags.txt', 'r') as f:
        #     tagsl = [line.strip() for line in f]

        # with open(r'url.txt', 'r') as f:
        #     data = f.read()
        #     urllist = [j.strip(" '") for j in [i.strip("'") for i in list(data.split(','))]]
        #     print(urllist)

        # self.tags = tagsl
        # self.tagsln = 180//len(tagsl)
        # print('len(tagsl)', self.tagsln)
        self.urls = []
        self.tpost = 0
        # self.turls = urllist
        self.loginbtn = ''

    def exit(self):
        bot = self.bot
        bot.quit()
        print('bot.quit()')

    def login(self):
        bot = self.bot
        bot.get('https://instagram.com/')
        time.sleep(3)
        if check_exists_by_xpath(bot, "//button[text()='Log In']"):
           print("skiped 1")
           return self.login()

        bot.find_element_by_xpath("//button[text()='Log In']").click()
        time.sleep(5)

        if check_exists_by_xpath(bot, "//button[text()='Accept']"):
            print("No cookies")
        else:
            bot.find_element_by_xpath("//button[text()='Accept']").click()
            print("Accepted cookies")

        time.sleep(4)
        print("Logging in...")
        time.sleep(1)
        if check_exists_by_xpath(bot, "//input[@name='username']"):
           print("skiped 1")
           return self.login()

        username_field = bot.find_element_by_xpath(
            "//input[@name='username']")
        username_field.send_keys(self.username)

        if check_exists_by_xpath(bot, "//input[@name='password']"):
           print("skiped 1")
           return self.login()

        find_pass_field = (
            By.XPATH, "//input[@name='password']")
        WebDriverWait(bot, 50).until(
            EC.presence_of_element_located(find_pass_field))
        pass_field = bot.find_element(*find_pass_field)
        WebDriverWait(bot, 50).until(
            EC.element_to_be_clickable(find_pass_field))
        pass_field.send_keys(self.password)

        self.loginbtn = "//button[text()='Log In']"

        if check_exists_by_xpath(bot, "//button[text()='Log In']"):
            self.loginbtn = "//a[text()='Log in']"

            if check_exists_by_xpath(bot, "//a[text()='Log in']"):
                print("set 3 link")
                self.loginbtn = "//div[text()='Log In']"
                
                if check_exists_by_xpath(bot, "//div[text()='Log In']"):
                    print("recall login")
                    return self.login()

            print("set 2 link")
            
        print(self.loginbtn)
        bot.find_element_by_xpath(
            self.loginbtn).click()
        time.sleep(5)
        if check_exists_by_xpath(bot, "//button[contains(@class,'aOOlW  bIiDR  ')]") == False:
            print("login error")
            error = bot.find_element_by_xpath("//h3[contains(@class,'_7UhW9     LjQVu     qyrsm KV-D4          uL8Hv         ')]").text
            return error 

        if check_exists_by_xpath(bot, "//p[@id='slfErrorAlert']") == False:
            print("login error")
            error = bot.find_element_by_xpath("//p[@id='slfErrorAlert']").text
            
            return error

        # bot.get('https://instagram.com/')
        if bot.title == "Login • Instagram":
            print(bot.title)
            error = "Login is not completed"
            return error
            
        return False


 

def check_exists_by_xpath(driver, xpath):
    try:
        driver.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return True

    return False