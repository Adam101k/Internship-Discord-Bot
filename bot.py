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

intents = discord.Intents.default()

MAIN_CHANNEL = None

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')
USER_DATA_DIR = os.getenv('USER_DATA_DIR')
USER_EMAIL = os.getenv('USER_EMAIL')
USER_PASSWORD = os.getenv('USER_PASSWORD')
CHANNEL_ID = int(os.getenv('CHANNEL_ID'))

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

        for job in jobs:
            title, company, picture, link = job

            embed = discord.Embed(title=title, url=link)
            embed.set_author(name=company)
            embed.set_thumbnail(url=picture)

            await MAIN_CHANNEL.send(embed=embed)

    await send_jobs()
    
bot.run(BOT_TOKEN)