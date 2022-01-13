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
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from helpers import db_user_querys as db_user
import schedule
from datetime import datetime
from pyvirtualdisplay import Display
 
 


class Bot:
    def __init__(self, user):
        if user['insta_ac']:
            self.data = db_user.user_full_data(user)
            self.username = self.data['insta']['insta_id']
            self.password = self.data['insta']['passwd']
        else:
            self.data = user
        display = Display(visible=0, size=(500, 950))
        display.start()  
        options = Options()
        options.headless = True
        options.add_argument("-no-sandbox")
        user_agent = "Mozilla/5.0 (iPhone; U; CPU iPhone OS 3_0 like Mac OS X; en-us) AppleWebKit/528.18 (KHTML, like Gecko) Version/4.0 Mobile/7A341 Safari/528.16"
        options.set_preference("general.useragent.override", user_agent)

        self.bot = webdriver.Firefox(options=options,executable_path=os.environ.get("GECKODRIVER_PATH"), firefox_binary=FirefoxBinary(os.environ.get("FIREFOX_BIN")))
        self.bot.set_window_size(500, 950)


        self.tags = self.data['tags']
        self.tagsln = 180//len(self.data['tags'])
        print('len(tagsl)', self.tagsln)
        try:
            if self.data['urls']:
                self.turls = self.data['urls']
            print(self.turls)
        except:
            self.turls = []
            print('no urls')

        self.tpost = 0
        self.todaylinks = []
        self.urls = []
        self.loginbtn = ''
        self.comments =  self.data['comments']

    def exit(self):
        bot = self.bot
        bot.quit()
        print('bot.quit()')

    def login(self,username = None, password = None):
        if username and password:
            self.username = username
            self.password = password
        
        print(self.username,self.password)
        bot = self.bot
        bot.get('https://instagram.com/')
        time.sleep(3)
        if check_exists_by_xpath(bot, "//button[text()='Log In']"):
           print("skiped 1")
           return self.login()

        bot.find_element(By.XPATH, "//button[text()='Log In']").click()
        time.sleep(5)

        if check_exists_by_xpath(bot, "//button[text()='Accept']"):
            print("No cookies")
        else:
            bot.find_element(By.XPATH, "//button[text()='Accept']").click()
            print("Accepted cookies")

        time.sleep(4)
        print("Logging in...")
        time.sleep(1)
        if check_exists_by_xpath(bot, "//input[@name='username']"):
           print("skiped 1")
           return self.login()

        username_field = bot.find_element(
            By.XPATH, "//input[@name='username']")
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
                self.loginbtn = "//div[text()='Log In']"
                
                if check_exists_by_xpath(bot, "//div[text()='Log In']"):
                    print("recall login")
                    return self.login()

            
            
        
        bot.find_element(
            By.XPATH, self.loginbtn).click()
        time.sleep(5)
        if check_exists_by_xpath(bot, "//button[contains(@class,'aOOlW  bIiDR  ')]") == False:
            print("login error")
            error = bot.find_element(By.XPATH, "//h3[contains(@class,'_7UhW9     LjQVu     qyrsm KV-D4          uL8Hv         ')]").text
            return error 

        if check_exists_by_xpath(bot, "//p[@id='slfErrorAlert']") == False:
            print("login error")
            error = bot.find_element(By.XPATH, "//p[@id='slfErrorAlert']").text
            
            return error

        if bot.title == "Login • Instagram":
            error = "Login is not completed"
            print(bot.title)  
            return error

        time.sleep(3)
        bot.get('https://www.instagram.com/explore/tags/insta')
        if check_exists_by_xpath(bot, "//a[contains(@class,'ablfq')]") == False:
            error = "Login is not completed"
            return error

        return False

    def get_posts(self):
        print('Searching post by tag...')
        bot = self.bot
    
        tags = self.tags
        print(tags)
        if tags == []:
               print("Finished")
               self.exit()
               return

        tag = tags.pop()
        link = 'https://www.instagram.com/explore/tags/' + tag
        bot.get(link)
        
        if check_exists_by_xpath(bot, "//a[contains(@class,'ablfq')]") == False:
            print("set 3 error")
            self.login()
            return self.get_posts()

        time.sleep(4)

        for i in range(10):
            ActionChains(bot).send_keys(Keys.END).perform()
            time.sleep(2)

        divs = bot.find_elements(By.XPATH, "//a[@href]")
        first_urls = []

        for i in divs:
            if i.get_attribute('href') != None:
                first_urls.append(i.get_attribute('href'))
            else:
                continue
        
        for url in first_urls:
            if url.startswith('https://www.instagram.com/p/'):
                if url not in self.turls:
                    self.urls.append(url)

                print(len(self.urls))
                if len(self.urls) == self.tagsln:
                    break

        self.tpost += int(len(self.urls))
        print('self.totalpost----1',self.tpost)
        return self.comment(random_comment(self.comments))


    def comment(self, comment):
        print(len(self.urls))
       
        if len(self.urls) == 0:
            print('Finished tag jumping to next one...')
            
            time.sleep(3000)
            return self.get_posts()
            # return run.get_posts()

        bot = self.bot
        url = self.urls.pop()

        print(f'Geting post : {url}')
        bot.get(url)
        bot.implicitly_wait(1)

        bot.execute_script("window.scrollTo(0, window.scrollY + 300)")
        time.sleep(3)

        if check_exists_by_xpath(bot, "//span[contains(@class,'fr66n')]/button"):
           print("skiped 0")
           return self.comment(random_comment(self.comments))

        bot.find_element(
            By.XPATH, "//span[contains(@class,'fr66n')]/button").click()
        time.sleep(3)
        print('liked......!')

        if check_exists_by_xpath(bot, "//span[contains(@class,'_15y0l')]/button"):
           print("skiped 1")
           return self.comment(random_comment(self.comments))

        bot.find_element(
            By.XPATH, "//span[contains(@class,'_15y0l')]/button").click()

        time.sleep(3)
        if check_exists_by_xpath(bot, "//form/textarea"):
            print("skiped 2")
            return self.comment(random_comment(self.comments))

        time.sleep(4)
        bot.find_element(
            By.XPATH, "//form/textarea").click()
       
        self.turls.append(url)
        self.todaylinks.append(url)
        db_user.insta_url_add(self.data, [self.turls,self.todaylinks])
        print(self.turls)
        time.sleep(4)
        find_comment_box = (
            By.XPATH, '//textarea[@Placeholder = "Add a comment…"]')
        WebDriverWait(bot, 50).until(
            EC.presence_of_element_located(find_comment_box))
        comment_box = bot.find_element(*find_comment_box)
        WebDriverWait(bot, 50).until(
            EC.element_to_be_clickable(find_comment_box))
        comment_box.click()
        time.sleep(10)
        comment_box.send_keys(comment)

        print('commenting...')

        find_post_button = (
            By.XPATH, "//button[text()='Post']")
        WebDriverWait(bot, 50).until(
            EC.presence_of_element_located(find_post_button))
        post_button = bot.find_element(*find_post_button)
        WebDriverWait(bot, 50).until(
            EC.element_to_be_clickable(find_post_button))
        post_button.click()
        # edit this line to make bot faster
        time.sleep(120)
        # ---------------------------------

        return self.comment(random_comment(self.comments))


    def do_job(self):
        x = datetime.now()
        status = True
        days = days_between(self.data['start_date'], x.strftime("%d-%m-%Y"))
        if days > 30:
            print("date ended")
            status = False
            self.data['status'] = False
            self.data['bot'] = False
            db_user.time_out(self.data)
        elif days == 0:
            status = False
        
        if status:
            try:
                self.data = db_user.user_full_data(self.data)
                try:
                    if self.data['t-date']:
                        self.data['t-date'][x.strftime("%d-%m-%Y")] = 0
                except:
                    self.data['t-date'] = {x.strftime("%d-%m-%Y"):0}
                    print('no t-date')

                db_user.set_date(self.data)
                self.login()
                self.get_posts()
                self.exit()
                return
            except:
                db_user.bot_run_fail(self.data)
                print("error do_job")
                return


    def run_bot(self):
        x = datetime.now()
        status = True
        try:
            if self.data['start_date']:
                pass

        except:
            self.data['start_date'] = x.strftime("%d-%m-%Y")
            db_user.add_start_date(self.data)
            try:
                if self.data['t-date']:
                    self.data['t-date'][x.strftime("%d-%m-%Y")] = 0
            except:
                self.data['t-date'] = {x.strftime("%d-%m-%Y"):0}
                print('no t-date')

            db_user.set_date(self.data)
            try:
                self.login()
                self.get_posts()
                self.exit()
            except:
                db_user.bot_run_fail(self.data)
                print("error do_job")


        schedule.every().day.at("01:30").do(self.do_job)
        while self.data['bot']:
            schedule.run_pending()
            time.sleep(1)



def random_comment(comments):
    comment = random.choice(comments)
    return comment
 

def check_exists_by_xpath(driver, xpath):
    try:
        driver.find_element(By.XPATH, xpath)
    except NoSuchElementException:
        return True

    return False


def days_between(d1, d2):
    d1 = datetime.strptime(d1, "%d-%m-%Y")
    d2 = datetime.strptime(d2, "%d-%m-%Y")
    return abs((d2 - d1).days)
