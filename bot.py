import discord
from discord.ext import tasks, commands
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
from dotenv import load_dotenv
import scraper
import os
import json

intents = discord.Intents.default()

MAIN_CHANNEL = None

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')
USER_DATA_DIR = os.getenv('USER_DATA_DIR')
USER_EMAIL = os.getenv('USER_EMAIL')
USER_PASSWORD = os.getenv('USER_PASSWORD')
CHANNEL_ID = 1138319147705569331

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print('Bot is ready.')

    global MAIN_CHANNEL
    MAIN_CHANNEL = bot.get_channel(CHANNEL_ID)

    linkedin_login()
    await monitor_linkedin() #begins LinkedIn scraping process

def linkedin_login():
    opts = Options()
    opts.add_argument('user-data-dir=' + USER_DATA_DIR)
    driver = webdriver.Chrome(options=opts, service=Service(executable_path=ChromeDriverManager().install()))

    #navigates to page at given URL
    driver.get('https://www.linkedin.com')

    #signing into LinkedIn
    try:
        username_box = driver.find_element(By.ID, 'session_key')
        username_box.send_keys(USER_EMAIL)

        sleep(0.5)

        password_box = driver.find_element(By.ID, 'session_password')
        password_box.send_keys(USER_PASSWORD)

        sleep(0.5)

        sign_in_button = driver.find_element(By.XPATH, '//*[@type="submit"]')
        sign_in_button.click()
        sleep(15)
    except: #if already logged into LinkedIn, ends login process
        return

#begins LinkedIn scraping process
async def monitor_linkedin():
    #gets list of jobs on page from scraper.py and sends each in an Embed
    async def send_jobs():
        jobs = scraper.get_jobs()

        await MAIN_CHANNEL.send('# of jobs scraped:' + str(len(jobs)))

        posted_jobs_file = get_posted_jobs()
        posted_jobs = set(posted_jobs_file['posted_jobs'])

        num_new_jobs = 0
        for job in jobs:
            title, company, picture, link = job

            job_post_id = title + company
            if job_post_id in posted_jobs: #skips job if it was already posted
                continue

            num_new_jobs += 1
            posted_jobs_file['posted_jobs'].append(job_post_id)
            posted_jobs.add(job_post_id)

            embed = discord.Embed(title=title, url=link)
            embed.set_author(name=company)
            embed.set_thumbnail(url=picture)

            await MAIN_CHANNEL.send(embed=embed)
        
        save_posted_jobs(posted_jobs_file)
        await MAIN_CHANNEL.send(str(num_new_jobs) + " new jobs")

    while True:
        await MAIN_CHANNEL.send('Getting new job posts...')
        await send_jobs()
        await MAIN_CHANNEL.send('Waiting for 12 hours...')
        sleep(60 * 60 * 12) #sleep for 12 hours

#gets json file of posted jobs
def get_posted_jobs():
    with open('./posted_jobs.json') as file:
        posted_jobs = json.load(file)
        return posted_jobs

#writes to and saves json file of posted jobs
def save_posted_jobs(posted_jobs_file):
    with open('./posted_jobs.json', 'w') as file:
        file.seek(0)
        json.dump(posted_jobs_file, file, indent=4)
        file.truncate()
    
bot.run(BOT_TOKEN)