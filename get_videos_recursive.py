import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup
import time

def get_first_recommendation(url, driver, depth=5, current_depth=0, visited=None, recommendations=None):
    if visited is None:
        visited = set()
    if recommendations is None:
        recommendations = []
    
    if current_depth >= depth:
        return recommendations
    
    try:
        driver.get(url)
        time.sleep(5)
        button = driver.find_element(by='xpath', value='//*[@id="login-pannel"]/div[2]')
        button.click()
        
        time.sleep(5)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        
        # 检查页面是否有指定文本的标题，如果有则打印并结束递归
        if soup.find('h2', class_="wLIXf65T").text != "推荐视频":
            print(soup.find('h2', class_="wLIXf65T").text)
            return recommendations

        section = soup.find('div', class_="fYHWqVWk")
        a_tag = section.find('a', class_='hY8lWHgA')
        if a_tag and 'href' in a_tag.attrs:
            vid = str('https:' + a_tag['href'])
    
        # 获取第一个推荐视频并递归获取其推荐视频列表
        if vid:
            deeper_recommendations = get_first_recommendation(vid, driver, depth, current_depth + 1, visited, recommendations)
            recommendations = [vid] + deeper_recommendations
    except Exception as e:
        print("An error occurred while fetching recommendations for", url)
        print(e)
    
    return recommendations

# 读取 CSV 文件
df = pd.read_csv("/home/jingjie/Desktop/Projects/DouyinScraper/outputs/seed.csv")

# 设置 Chrome WebDriver 选项
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")  # 启动时最大化窗口
driver = webdriver.Chrome(options=options)

# 遍历 CSV 中的每个 URL，并获取推荐视频列表
recommendations_list = []
for url in df['url']:
    recommendations = get_first_recommendation(url, driver)
    recommendations_list.append(recommendations)

# 将推荐视频列表添加到 DataFrame 中
df['recommendations'] = recommendations_list
df['complete'] = [len(recommendations) == 5 for recommendations in df['recommendations']]

# 关闭 WebDriver
driver.quit()

# 保存修改后的 DataFrame 到新的 CSV 文件中
df.to_csv("/outputs/data.csv", index=False)
