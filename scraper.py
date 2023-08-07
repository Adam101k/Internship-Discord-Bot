import pandas as pd
from parsel import Selector
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
opts = Options()

driver = webdriver.Chrome(options=opts, executable_path='chromedriver')

#navigates to page at given URL
driver.get('https://www.linkedin.com')

#gets HTML element for the email input box on the sign in screen
username = driver.find_element(By.ID, 'session_key')

#enters email into the input box
username.send_keys('email')