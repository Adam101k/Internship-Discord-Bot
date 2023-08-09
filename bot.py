import discord
from discord.ext import tasks, commands
from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup

intents = discord.Intents.default()

bot = commands.Bot(command_prefix='!', intents=intents)

internships = []

@tasks.loop(seconds=30)
async def check_internships():
    print("Starting bot...")
    url = 'https://www.linkedin.com/jobs/intern-software-engineer-jobs'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    print("Scraping LinkedIn...")
    new_listings = []
    print("Coopabyte")
    title = soup.select_one(".base-search-card__title").text
    company = soup.select_one('.base-search-card__subtitle').text
    date = soup.select_one('.job-search-card__listdate').text
        
    internship = {'title': title, 'company': company, 'date': date}
    if internship not in internships:
            new_listings.append(internship)
    
    for internship in new_listings:
        print("Posting new internships...")
        internships.append(internship)
        channel = bot.get_channel(1138319147705569331) # channel ID
        await channel.send(f"New Internship:\n{internship['title']}\n{internship['company']}\nListed on: {internship['date']}") 
@bot.event
async def on_ready():
    check_internships.start()
    print('Bot is ready.')
    
bot.run('NzYzOTk3ODkwNzY2NDM4NDAx.GjuWeO.tacljJO8Iwb_VwYLWqQjtDq3JX9AZoVQBCiMYk')