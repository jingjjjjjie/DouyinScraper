from selenium.webdriver import Chrome
from selenium.webdriver import ChromeOptions
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time 
import os
from utils.ttshitu import base64_api
import base64
import json
import requests
import random
import csv

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
        action.move_to_element_with_offset(image, x, y).click().perform()
        sleep_duration = random.uniform(1, 1.5)
        time.sleep(sleep_duration)
    
    time.sleep(3)
    button = driver.find_element(by="xpath", value='//*[@id="vc_captcha_box"]/div/div/div[3]/div[2]/div')
    button.click()
    driver.switch_to.default_content()

def get_page_html(driver):
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    return soup

# # Get the total number of sections
# # 'MgWTwktU search-result-card B9KMVC9A'
# note_sections = soup.find_all('li', class_='MgWTwktU search-result-card B9KMVC9A')
# data_list = []
# total_sections = len(note_sections)
# print(total_sections)

# for index, note_section in enumerate(note_sections, start=1):
#     print(index)

def scroll(driver, count):
    scroll_size = 400
    c = 0
    while c < count:
        driver.execute_script('window.scrollTo(0, arguments[0]);', scroll_size)
        scroll_size += 400
        c+=1
        time.sleep(1)

if __name__ == "__main__":
    #url = "https://www.douyin.com/search/%E5%90%AC%E5%88%B0%E6%98%A5%E5%A4%A9%E7%9A%84%E6%B6%88%E6%81%AF?publish_time=0&sort_type=0&type=video"
    url = "https://www.douyin.com/search/%E6%88%91%E5%9B%BD%E6%98%A5%E8%80%95%E5%A4%87%E8%80%95%E7%94%B1%E5%8D%97%E5%90%91%E5%8C%97%E5%B1%95%E5%BC%80?publish_time=0&sort_type=0&type=video"
    options = ChromeOptions()
    #options.add_argument("--headless=new")
    options.add_experimental_option("detach", True)
    chrome_driver_path = './chromedriver'
    service = Service(chrome_driver_path)
    # Pass the service object to the Chrome driver
    driver = Chrome(options=options, service=service)
    action = ActionChains(driver)
    driver.get(url)
    
    time.sleep(5)
    img_screenshot_64 = switch_iframe_and_screenshot(driver)

    time.sleep(1)
    coords = base64_api(uname='jingjjjjjie', pwd='Beida123', img=img_screenshot_64, typeid=27)
    
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="captcha_click_image"]')))
    click_on_captcha(driver, action, coordininates=coords)

    time.sleep(5)
    scroll(driver,count=200)

    time.sleep(10)
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Open a file for writing (this will create the file if it doesn't exist)
    with open('./output.txt', 'w') as file:
        # Write the text to the file
        file.write(str(soup))

    seed_list = []

    sections = soup.find_all('li', class_ ="MgWTwktU search-result-card B9KMVC9A")
    print(len(sections))

    for section in sections:
        # Initialize an empty dictionary to store data for each section
        data = {}

        # Extract the href attribute from the <a> tag
        a_tag = section.find('a', class_='B3AsdZT9 AqS8FEQL')
        if a_tag and 'href' in a_tag.attrs:
            data['url'] = 'https:' + a_tag['href']

        # Extract the specific div text you're interested in
        specific_div = section.find('div', class_='swoZuiEM')
        if specific_div:
            data['description'] = specific_div.get_text(strip=True)

        # Check if data was extracted and if so, append to the seed_list
        if data:
            seed_list.append(data)

    # Optional: print or process the seed_list further
    print(seed_list)

    # Define the fieldnames based on the dictionary keys
# Assuming all dictionaries have the same structure
    fieldnames = seed_list[0].keys() if seed_list else []

    # Write to CSV
    with open("./outputs/seed.csv", mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        # Write the header
        writer.writeheader()

        # Write the rows
        for seed in seed_list:
            writer.writerow(seed)

    print(f"Data successfully written to seed.csv")