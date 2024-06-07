from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import random
import time
import json
import requests

def find_and_click(driver,xpath,sleep=True):
    if sleep:
        time.sleep(random.randint(1, 3))
    elem = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.XPATH, xpath))
    )
    elem = driver.find_element(By.XPATH, xpath)
    elem.click()

def find_and_type(driver,xpath,text,sleep=True):
    if sleep:
        time.sleep(random.randint(1, 3))
    elem = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.XPATH, xpath))
    )
    elem = driver.find_element(By.XPATH, xpath)
    elem.send_keys(text)

def wait_to_find(driver, xpath, wait_time):
    elem = WebDriverWait(driver, wait_time).until(
    EC.visibility_of_element_located((By.XPATH, xpath))
    )
    try:
        driver.find_element(By.XPATH, xpath)
    except NoSuchElementException:
        return False
    
    return True

def find_elem_pos_and_size(driver,xpath):
    elem = driver.find_element(By.XPATH, xpath)

    return elem.location, elem.size

def check_exists_by_xpath(driver,xpath):
    try:
        driver.find_element(By.XPATH, xpath)
    except NoSuchElementException:
        return False
    
    return True

def find_by_selector_and_click(driver,selector):
    elem = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.CSS_SELECTOR, selector))
    )
    elem = driver.find_element(By.CSS_SELECTOR, selector)
    elem.click()

def wait_to_find_by_selector(driver, selector, wait_time):
    elem = WebDriverWait(driver, wait_time).until(
    EC.visibility_of_element_located((By.CSS_SELECTOR, selector))
    )
    try:
        driver.find_element(By.CSS_SELECTOR, selector)
    except NoSuchElementException:
        return False
    
    return True

def get_rating(host,port,images,race,rating):
    data=json.dumps({'images': images})
    
    url = f'http://{host}:{port}/rating?race={race}&rating={rating}'
    response = requests.post(url, data=data, headers={'content-type': 'application/json'})
    return json.loads(response.text)