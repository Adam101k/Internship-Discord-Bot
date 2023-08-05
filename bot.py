import discord
import data_pull

def run_discord_bot():
    TOKEN = 'ODQ5NDU1NjU4NTYxNDM3NzA3.GHIYQB.dyPt2P-4C8kndnKg6D3noab4xjr1Klra2N7INs'
    client = discord.Client(intents=discord.Intents.default())

    @client.event
    async def on_ready():
        print(f'{client.user} is no running!')

    client.run(TOKEN)
