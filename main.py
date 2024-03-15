from selenium.webdriver import Chrome
from selenium.webdriver import ChromeOptions
from bs4 import BeautifulSoup
import time 
from ttshitu import base64_api

options = ChromeOptions()
#options.add_argument("--headless=new")
options.add_experimental_option("detach", True)
driver = Chrome(options=options)
url = "https://www.douyin.com/search/%E5%90%AC%E5%88%B0%E6%98%A5%E5%A4%A9%E7%9A%84%E6%B6%88%E6%81%AF?publish_time=0&sort_type=0&type=video"
driver.get(url)


#switch to captcha's iframe
time.sleep(5)
iframe = driver.find_element(by='xpath', value='//*[@id="root"]/iframe')
driver.switch_to.frame(iframe)

#get captcha image 
img = driver.find_element(by="xpath", value='//*[@id="vc_captcha_box"]/div/div/div[1]/div')

#screenshotcaptcha
img = driver.find_element(by="xpath", value='/html/body/div/div/div/div/div[2]/img')
img_screenshot = img.screenshot_as_png
time.sleep(2)
result = base64_api(uname='jingjjjjjie', pwd='Beida123', img=img_screenshot, typeid=27)
print(result)

#找到视频按钮
time.sleep(2)
button = driver.find_element(by="xpath", value='//*[@id="search-content-area"]/div/div[1]/div[1]/div[1]/div[2]/span[2]')
button.click()


html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

# Get the total number of sections
# 'MgWTwktU search-result-card B9KMVC9A'
note_sections = soup.find_all('li', class_='MgWTwktU search-result-card B9KMVC9A')
data_list = []
total_sections = len(note_sections)
print(total_sections)

for index, note_section in enumerate(note_sections, start=1):
    print(index)

