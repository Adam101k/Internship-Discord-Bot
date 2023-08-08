import discord
import data_pull
import os
from os.path import join, dirname
from dotenv import load_dotenv

def run_discord_bot():
    dotenv_path = join(dirname(__file__), '.env')
    load_dotenv(dotenv_path)

    TOKEN = os.environ.get("DISCORD_TOKEN")
    client = discord.Client(intents=discord.Intents.default())

    @client.event
    async def on_ready():
        print(f'{client.user} is no running!')

    client.run(TOKEN)
