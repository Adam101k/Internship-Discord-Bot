import discord
from discord.ext import commands 

intents = discord.Intents.default() 
intents.messages = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.command()
async def scrape(ctx):
  await bot.cogs["internship_scraper"].scrape_internships()
@bot.event
async def on_ready():
    print('Bot ready!')
    
bot.load_extension('internship_scraper') 

bot.run('NzYzOTk3ODkwNzY2NDM4NDAx.GjuWeO.tacljJO8Iwb_VwYLWqQjtDq3JX9AZoVQBCiMYk')
bot.load_extension('internship_scraper')
print('got here')