#!/usr/bin/env python3
import sys
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from getpass import getpass
from PIL import Image
from io import BytesIO
import base64
import traceback
from input_args import get_input_args
from remote_server.remote_selenium_server import selenium_server
from utility_functions import *
from tinder_functions import get_tinder_api_request, post_tinder_api_request
import os
from dotenv import load_dotenv
load_dotenv()

FB_USERNAME = os.environ.get("FB_USERNAME")
FB_PASSWORD = os.environ.get("FB_PASSWORD")

class TinderBotV1():
    def __init__(self,driver,host,port,human_login,use_api,min_rating,pref_race):
        self.url = 'https://tinder.com/'
        self.driver = driver
        self.host = host
        self.port = port
        self.human_login = human_login
        self.use_api = use_api
        self.min_rating = min_rating
        self.pref_race = pref_race
    
    def login(self):
        driver = self.driver
        human_login = self.human_login

        driver.get(self.url)
        driver.maximize_window()

        if human_login:
            time.sleep(70)
        else:
            if not FB_USERNAME or not FB_PASSWORD:
                print('Enter Facebook Username:')
                fb_username = input()
                print('Enter Facebook Password:')
                fb_password = getpass()
            else:
                fb_username = FB_USERNAME
                fb_password = FB_PASSWORD
            
            find_and_click(driver, '/html/body/div[1]/div/div[2]/div/div/div[1]/div[1]/button/div[2]')
            find_and_click(driver,'/html/body/div[1]/div/div[1]/div/main/div[1]/div/div/div/div/header/div/div[2]/div[2]/a/div[2]')
            find_and_click(driver,'/html/body/div[2]/main/div/div[1]/div/div/div[3]/span/div[2]/button')

            base_window = driver.window_handles[0]
            facebook_window = driver.window_handles[1]

            driver.switch_to.window(facebook_window)
            find_and_type(driver, '//*[@id="email"]', fb_username)
            find_and_type(driver, '//*[@id="pass"]', fb_password)
            find_and_click(driver, '/html/body/div/div[2]/div[1]/form/div/div[3]/label[2]/input')
            time.sleep(3)

            driver.switch_to.window(base_window)

            find_and_click(driver,'/html/body/div[2]/main/div/div/div/div[3]/button[1]')
            find_and_click(driver, '/html/body/div[2]/main/div/div/div/div[3]/button[1]')

            time.sleep(10)
        
    def get_match_images_and_swipe(self,likes,like_limit):
        driver = self.driver
        use_api = self.use_api

        if use_api:
            local_storage = driver.execute_script('return window.localStorage;')
            api_token = local_storage['TinderWeb/APIToken']
            url = 'https://api.gotinder.com/v2/recs/core'
            data = get_tinder_api_request(url,api_token)
            for i in data['data']['results']:
                if likes < like_limit:
                    user_id = i['user']['_id']
                    images = []
                    for y in i['user']['photos']:
                        img_url = y['processedFiles'][0]['url']
                        images.append(img_url)

                    print(i['user']['name'])
                    likes += self.match_decision(images,user_id,api_token)
                else:
                    break
                
            return likes
        else:
            window = driver.get_window_size()
            
            loc,size = find_elem_pos_and_size(driver,'/html/body/div[1]/div/div[1]/div/main/div[1]/div/div/div[1]/div/div/div[2]/div[1]')
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            div = soup.select('#o-98920890 > div > div.App__body.H\(100\%\).Pos\(r\).Z\(0\) > div > main > div.H\(100\%\) > div > div > div.Mt\(a\).Px\(4px\)--s.Pos\(r\).Expand.H\(--recs-card-height\)--ml.Maw\(--recs-card-width\)--ml > div > div > div.Toa\(n\).Bdbw\(--recs-gamepad-height\).Bdbc\(t\).Bdbs\(s\).Bgc\(\#000\).Wc\(\$transform\).Prs\(1000px\).Bfv\(h\).Ov\(h\).W\(100\%\).StretchedBox.Bdrs\(8px\) > div.Expand.D\(f\).Pos\(r\).tappable-view.Cur\(p\) > div.CenterAlign.D\(f\).Fxd\(r\).W\(100\%\).Px\(8px\).Pos\(a\).TranslateZ\(0\)')
            try:
                buttons = div[0].find_all('button')
            except:
                buttons = [1]
            
            if window['width'] <= 1440 and window['height'] <= 875:
                left = loc['x']+700
                top = loc['y']
                right = loc['x']+1100 + size['width']
                bottom = loc['y'] + size['height']+400
            else:
                left = loc['x']
                top = loc['y']
                right = loc['x'] + size['width']
                bottom = loc['y'] + size['height']

            if check_exists_by_xpath(driver, '/html/body/div[2]/main/div/button[2]'):
                find_and_click(driver, '/html/body/div[2]/main/div/button[2]')

            images = []
            for i in range(1,len(buttons)+1):
                if len(buttons) > 1:
                    find_and_click(driver,f'/html/body/div[1]/div/div[1]/div/main/div[1]/div/div/div[1]/div/div/div[3]/div[1]/div[2]/button[{i}]', False)
                time.sleep(0.5)
                png = driver.get_screenshot_as_png()
                im = Image.open(BytesIO(png))
                im = im.crop((left, top, right, bottom))
                rgb_im = im.convert('RGB')
                buffered = BytesIO()
                rgb_im.save(buffered, format="JPEG")
                # rgb_im.save(f"img_{i}.png","PNG")
                img_str = base64.b64encode(buffered.getvalue())
                images.append(img_str.decode('utf-8'))
            
            likes = self.match_decision(images)

            return likes
    
    def match_decision(self,images,user_id=None,api_token=None):
        driver = self.driver
        host = self.host
        port = self.port
        use_api = self.use_api
        min_rating = self.min_rating
        pref_race = self.pref_race

        rating = get_rating(host=host,port=port,images=images,race=pref_race,rating=min_rating)
        print(rating)

        if use_api:
            if rating['match']:
                post_tinder_api_request(f'https://api.gotinder.com/like/{user_id}?locale=en', api_token)
                return 1
            else:
                get_tinder_api_request(f'https://api.gotinder.com/pass/{user_id}?locale=en',api_token)
                return 0
        else:
            if rating['match']:
                find_by_selector_and_click(driver,'#o-98920890 > div > div.App__body.H\(100\%\).Pos\(r\).Z\(0\) > div > main > div.H\(100\%\) > div > div > div.Mt\(a\).Px\(4px\)--s.Pos\(r\).Expand.H\(--recs-card-height\)--ml.Maw\(--recs-card-width\)--ml > div > div > div.Pos\(a\).B\(0\).Iso\(i\).W\(100\%\).Start\(0\).End\(0\) > div > div.Mx\(a\).Fxs\(0\).Sq\(70px\).Sq\(60px\)--s.Bd.Bdrs\(50\%\).Bdc\(\$c-ds-border-gamepad-like-default\)')
                return 1
            else:
                find_by_selector_and_click(driver,'#o-98920890 > div > div.App__body.H\(100\%\).Pos\(r\).Z\(0\) > div > main > div.H\(100\%\) > div > div > div.Mt\(a\).Px\(4px\)--s.Pos\(r\).Expand.H\(--recs-card-height\)--ml.Maw\(--recs-card-width\)--ml > div > div > div.Pos\(a\).B\(0\).Iso\(i\).W\(100\%\).Start\(0\).End\(0\) > div > div.Mx\(a\).Fxs\(0\).Sq\(70px\).Sq\(60px\)--s.Bd.Bdrs\(50\%\).Bdc\(\$c-ds-border-gamepad-nope-default\)')
                return 0

if __name__ == '__main__':
    try:
        platform = sys.platform
        args = get_input_args()
        remote = args.remote
        host = args.host
        port = args.port
        human_login = args.human_login
        use_api = args.use_api
        pref_race = args.pref_race
        min_rating = args.min_rating
        like_limit = args.like_limit

        if platform == 'darwin':
            if remote:
                selenium_server()
                driver = webdriver.Remote(command_executor='http://localhost:4444/wd/hub', desired_capabilities=webdriver.DesiredCapabilities.CHROME)
            else:
                driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        elif platform == 'linux':
            if remote:
                selenium_server()
                driver = webdriver.Remote(command_executor='http://localhost:4444/wd/hub', desired_capabilities=webdriver.DesiredCapabilities.CHROME)
            else:
                driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

        tinder_bot = TinderBotV1(driver,host,port,human_login=human_login,use_api=use_api,pref_race=pref_race,min_rating=min_rating)
        tinder_bot.login()
        likes = 0
        while likes < like_limit:
            likes += tinder_bot.get_match_images_and_swipe(likes, like_limit)
            print(likes)
    except:
        print(traceback.print_exc())
    finally:
        try:
            driver.quit()
        except:
            pass