import pandas as pd
from parsel import Selector
from time import sleep
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.actions.wheel_input import ScrollOrigin
from selenium.webdriver.common.keys import Keys

from selenium.webdriver import ActionChains
from dotenv import load_dotenv
import os


load_dotenv()
USER_DATA_DIR = os.getenv('USER_DATA_DIR')
LINKEDIN_URL = os.getenv('LINKEDIN_URL')

def get_jobs():
    opts = Options()
    opts.add_argument('user-data-dir=' + USER_DATA_DIR)
    driver = webdriver.Chrome(options=opts, service=Service(executable_path=ChromeDriverManager().install()))

    #navigates to given url
    driver.get(LINKEDIN_URL)
    sleep(5)

    #scrolls down job list 5 times to load all postings
    job_list_element = driver.find_element(By.CSS_SELECTOR, ".jobs-search-results-list")
    for i in range(5):
        #scrolls from center of the job list
        ActionChains(driver).scroll_from_origin(ScrollOrigin.from_element(job_list_element), 0, 1000).perform()
        sleep(1)

    jobs = []
    
    #list of every HTML container of each job posting on the page
    job_posts = driver.find_elements(By.CSS_SELECTOR, ".job-card-container") 
    for job_post in job_posts:
        title = job_post.find_element(By.CSS_SELECTOR, ".job-card-list__title").text
        company = job_post.find_element(By.CSS_SELECTOR, ".job-card-container__primary-description").text
        # date = job_post.find_element('??').text
        picture = job_post.find_element(By.CSS_SELECTOR, "img.ember-view").get_attribute('src')
        link = job_post.find_element(By.CSS_SELECTOR, "a.job-card-list__title").get_attribute('href').split('?eBP')[0]
        jobs.append((title, company, picture, link))

    driver.quit()
    return jobs

    