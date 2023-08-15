from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd
import sendgrid
import os
import requests 
from selenium.webdriver.common.by import By

class LevelsFyi:
    def __init__(self):

        self.URL = 'https://www.levels.fyi/still-hiring/'
        page = requests.get(self.URL)

        self.jobs = []
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        self.soup = BeautifulSoup(page.content, "html.parser")

    def scrape_pay(self):
        table = self.soup.find("table", attrs={"class": "hiring-companies-table"})

        for row in table.find_all("tr")[1:]:
            try:
                company = row.find("th").text.strip()
                salary = company.find_element(By.CSS_SELECTOR, "expanded-salary-view_totalCompRowContainer__SsQ0H")
                time_posted = company.text
                print(salary)
            except:
                continue
    #wip