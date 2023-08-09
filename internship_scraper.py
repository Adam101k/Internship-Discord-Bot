import discord
from discord.ext import commands, tasks

# LinkedIn scraper methods
async def scrape_jobs():
   # Scrape LinkedIn
   return jobs
   
async def post_jobs(channel, jobs):
   # Post new jobs
   
# Cog
class JobScraper(commands.Cog):

  def __init__(self, bot):
    self.bot = bot
    
  @tasks.loop(hours=24)
  async def scrape_task(self):
    channel = bot.get_channel(1138319147705569331)
    jobs = await scrape_jobs()
    await post_jobs(channel, jobs)
      
  @commands.command()
  async def scrape(self, ctx):
    await self.scrape_task()
    
# Bot      
intents = discord.Intents.default()
intents.messages = True