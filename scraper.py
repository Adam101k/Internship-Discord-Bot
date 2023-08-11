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
    opts.add_argument('--incognito')
    driver = webdriver.Chrome(options=opts, service=Service(executable_path=ChromeDriverManager().install()))

    #navigates to given url
    driver.get(LINKEDIN_URL)
    sleep(5)

    #scrolls down job list 15 times to load all postings
    job_list_element = driver.find_element(By.CSS_SELECTOR, ".jobs-search__results-list")
    for i in range(10):
        #scrolls from center of the job list
        ActionChains(driver).scroll_from_origin(ScrollOrigin.from_element(job_list_element), 0, 5000).perform()
        sleep(1)

    jobs = []
    
    #list of every HTML container of each job posting on the page
    job_posts = driver.find_elements(By.CSS_SELECTOR, ".base-card") 
    for job_post in job_posts:
        title = job_post.find_element(By.CSS_SELECTOR, ".base-search-card__title").text
        company = job_post.find_element(By.CSS_SELECTOR, ".hidden-nested-link").text
        location = job_post.find_element(By.CSS_SELECTOR, ".job-search-card__location").text
        picture = job_post.find_element(By.CSS_SELECTOR, ".artdeco-entity-image").get_attribute('src')
        link = job_post.find_element(By.CSS_SELECTOR,'.base-card__full-link').get_attribute('href')

        time = job_post.find_element(By.XPATH, "//*[starts-with(@class, 'job-search-card__listdate')]")
        time_posted = time.text
        date = time.get_attribute('datetime')
        jobs.append((title, company, location, picture, link, time_posted, date))

    driver.quit()
    return jobs
    
if __name__ == "__main__":
    jobs = get_jobs()
    df = pd.DataFrame(jobs, columns=["Title", "Company", "Location", "Picture", "Link"])
    print(df.to_string())
