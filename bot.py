import discord
from discord.ext import tasks, commands
import datetime
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
CHANNEL_ID = int(os.getenv('CHANNEL_ID'))

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print('Bot is ready.')

    global MAIN_CHANNEL
    MAIN_CHANNEL = bot.get_channel(CHANNEL_ID)

    await monitor_linkedin() #begins LinkedIn scraping process

#begins LinkedIn scraping process
async def monitor_linkedin():
    #gets list of jobs on page from scraper.py and sends each in an Embed
    async def send_jobs():
        jobs = scraper.get_jobs()

        await MAIN_CHANNEL.send('#Number of jobs scraped:' + str(len(jobs)))

        posted_jobs_file = get_posted_jobs()
        posted_jobs = set(posted_jobs_file['posted_jobs'])

        #sorting jobs by date posted in descending order
        jobs = sorted(jobs, key=datetime_sort)

        num_new_jobs = 0
        num_duplicates = 0
        num_non_internships = 0
        for job in jobs:
            title, company, location, picture, link, time_posted, date = job

            formatted_time = date.strftime('%b %d')
            time = time_posted + ' - ' + formatted_time

            job_post_id = title + company
            if job_post_id in posted_jobs: #skips job if it was already posted
                num_duplicates += 1
                continue

            if not('intern' in title.lower() or 'internship' in title.lower()):
                num_non_internships += 1
                continue
            
            num_new_jobs += 1
            posted_jobs_file['posted_jobs'].append(job_post_id)
            posted_jobs.add(job_post_id)

            embed = discord.Embed(title=title, url=link)
            embed.set_author(name=company)
            embed.set_thumbnail(url=picture)
            embed.add_field(name='Location', value=location)
            embed.add_field(name='Date', value=time)

            await MAIN_CHANNEL.send(embed=embed)
        
        save_posted_jobs(posted_jobs_file)
        await MAIN_CHANNEL.send(str(num_new_jobs) + " new jobs")
        await MAIN_CHANNEL.send(str(num_duplicates) + " duplicate posts")
        await MAIN_CHANNEL.send(str(num_non_internships) + " non-internship posts")

    while True:
        await MAIN_CHANNEL.send('Getting new job posts...')
        await send_jobs()
        await MAIN_CHANNEL.send('Waiting for 12 hours...')
        sleep(60 * 60 * 12) #sleep for 12 hours

#key function for jobs sorting
def datetime_sort(tuple):
    time = tuple[-1]
    return time.timestamp()

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