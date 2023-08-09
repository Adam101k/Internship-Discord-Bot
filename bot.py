import discord
from discord.ext import tasks, commands
from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup

intents = discord.Intents.default()

bot = commands.Bot(command_prefix='!', intents=intents)





@bot.event
async def on_ready():
    print('Bot is ready.')
    linkedin_login()

def linkedin_login():
    #navigates to page at given URL
    driver.get('https://www.linkedin.com')

    #signing into LinkedIn
    username_box = driver.find_element(By.ID, 'session_key')
    username_box.send_keys(USER_EMAIL)

    sleep(0.5)

    password_box = driver.find_element(By.ID, 'session_password')
    password_box.send_keys(USER_PASSWORD)

    sleep(0.5)

    sign_in_button = driver.find_element(By.XPATH, '//*[@type="submit"]')
    sign_in_button.click()
    sleep(15)
    
bot.run('NzYzOTk3ODkwNzY2NDM4NDAx.GjuWeO.tacljJO8Iwb_VwYLWqQjtDq3JX9AZoVQBCiMYk')