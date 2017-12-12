#-- WEB SCRAPING --
import selenium
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

BASE_DIR = os.getcwd()
driver = webdriver.Chrome(executable_path=BASE_DIR+'\chromedriver')

driver.implicitly_wait(5)
# driver.maximize_window()

# navigate to the application home page
driver.get('https://es.ikariam.gameforge.com/')
driver.find_element_by_id("btn-login").click()
driver.implicitly_wait(30)

username = driver.find_element_by_id("loginName")
password = driver.find_element_by_id("loginPassword")

username.send_keys("user")
password.send_keys("pw")

driver.find_element_by_id("loginBtn").click()
for i in range(10):
    driver.get('view-source:https://s36-es.ikariam.gameforge.com/?view=island&islandId='+i)

    info = driver.find_element_by_tag_name('body').text
    file = open("workfile"+i,"w")
    file.write(info)
