from selenium.webdriver import Chrome
from selenium.webdriver import ChromeOptions
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time 
from utils.ttshitu import base64_api
import base64
import json
import requests
import random


def base64_api(uname, pwd, img, typeid):
    data = {"username": uname, "password": pwd, "typeid": typeid, "image": img, "remark": "点击两个形状相同的物体"}
    result = json.loads(
        requests.post("http://api.ttshitu.com/predict", json=data).text)
    if result['success']:
        return result["data"]["result"]
    else:
        #！！！！！！！注意：返回 人工不足等 错误情况 请加逻辑处理防止脚本卡死 继续重新 识别
        return result["message"]

def switch_iframe_and_screenshot(driver):                #switch to captcha's iframe and get element
    iframe = driver.find_element(by='xpath', value='//*[@id="root"]/iframe')
    driver.switch_to.frame(iframe)
    img = driver.find_element(by="xpath", value='//*[@id="captcha_click_image"]')
    img_screenshot_64 = img.screenshot_as_base64
    return img_screenshot_64, 

def click_on_captcha(driver, action, coordininates):
    for coord in coordininates.split("|"):
        x = int(coord.split(",")[0])
        y = int(coord.split(",")[1])
        print(x)
        print(y)
        image = driver.find_element(by="xpath", value='//*[@id="captcha_click_image"]')
        action.move_to_element_with_offset(image, 100, 100).click().perform()
        break
        #sleep_duration = random.uniform(1, 1.5)
        #time.sleep(sleep_duration)
    
    #time.sleep(sleep_duration)
    #button = driver.find_element(by="xpath", value='//*[@id="search-content-area"]/div/div[1]/div[1]/div[1]/div[2]/span[2]/')
    #button.click()

# #找到视频按钮
# time.sleep(2)
# button = driver.find_element(by="xpath", value='//*[@id="search-content-area"]/div/div[1]/div[1]/div[1]/div[2]/span[2]')
# button.click()


# html = driver.page_source
# soup = BeautifulSoup(html, 'html.parser')

# # Get the total number of sections
# # 'MgWTwktU search-result-card B9KMVC9A'
# note_sections = soup.find_all('li', class_='MgWTwktU search-result-card B9KMVC9A')
# data_list = []
# total_sections = len(note_sections)
# print(total_sections)

# for index, note_section in enumerate(note_sections, start=1):
#     print(index)


if __name__ == "__main__":
    url = "https://www.douyin.com/search/%E5%90%AC%E5%88%B0%E6%98%A5%E5%A4%A9%E7%9A%84%E6%B6%88%E6%81%AF?publish_time=0&sort_type=0&type=video"
    options = ChromeOptions()
    #options.add_argument("--headless=new")
    options.add_experimental_option("detach", True)
    driver = Chrome(options=options)
    url = url
    action = ActionChains(driver)
    driver.get(url)
    
    time.sleep(2)
    img_screenshot_64 = switch_iframe_and_screenshot(driver)

    time.sleep(5)
    coords = base64_api(uname='jingjjjjjie', pwd='Beida123', img=img_screenshot_64, typeid=27)
    
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="captcha_click_image"]')))
    click_on_captcha(driver, action, coordininates=coords)


    