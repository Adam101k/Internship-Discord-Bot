import discord 

# Import discord.py to use Discord API

from discord.ext import commands

# Import commands from discord.ext to create bot 

intents = discord.Intents.default()

# Create discord Intents to enable privileged intents

intents.messages = True  

# Explicitly enable reading messages

bot = commands.Bot(command_prefix='!', intents=intents)

# Create bot object with prefix '!' and specified intents

# Commands

@bot.command()  

# Decorator to mark function as a command

async def scrape(ctx):

    await bot.cogs["InternshipScraper"].scrape_internships()  
    # Call cog method to scrape internships

# Events 

@bot.event

async def on_ready():

    print('Bot ready!')
    
    bot.load_extension('internship_scraper')
    # Load cog on startup

# Run bot

bot.run('token')  

# Start bot with specified token

# Load cog

bot.load_extension('internship_scraper') 

print('got here')
# Print to confirm cog was loaded