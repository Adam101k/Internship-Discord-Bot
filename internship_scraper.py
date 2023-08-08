import requests
import time
import discord
from bs4 import BeautifulSoup
import logging
from datetime import timedelta
from discord.ext import tasks, commands

logger = logging.getLogger(__name__)

INTS_CACHE_TIME = timedelta(hours=6)

class InternshipScraper(commands.Cog):

    def __init__(self, bot):
        self.bot = bot 
        self.last_scraped = None
        self.internships = []

    def scrape_internships(self):
        """Scrape internships from LinkedIn"""
        url = "https://www.linkedin.com/jobs/search/?f_E=1&f_S=0&keywords=software%20engineering%20internship"
        response = requests.get(url)
        
        if response.status_code != 200:
            logger.error("Failed to scrape LinkedIn")
            return
        
        soup = BeautifulSoup(response.text, "html.parser")
        internship_elements = soup.find_all("li", class_="result-card")
        
        for element in internship_elements:
            # Extract data from each internship
            
             self.last_scraped = datetime.now()
             logger.info(f"Scraped {len(self.internships)} internships")
        
    def cache_expired(self):
        """Check if cache has expired"""
        if not self.last_scraped:
            return True
        now = datetime.now()
        return now - self.last_scraped > INTS_CACHE_TIME

    @tasks.loop(hours=24)
    async def post_internships(self):
        channel = self.bot.get_channel(config.CHANNEL_ID)
        
        if self.cache_expired():
            self.scrape_internships()
            
        new_ints = [i for i in self.internships if i["last_posted"] > self.last_posted]
        
        if new_ints:
            await channel.send("Today's new internships...")
            for i in new_ints:
                msg = f"**{i['title']}** at {i['company']} in {i['location']}"
                await channel.send(msg)
                
        self.last_posted = datetime.now()
        
def setup(bot):
    bot.add_cog(InternshipScraper(bot))