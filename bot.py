import discord
import data_pull

def run_discord_bot():
    TOKEN = 'ODQ5NDU1NjU4NTYxNDM3NzA3.GEmSUD.doEzJLk3riloGheoVIIbLfe-EhkGWJ1xOmxETk'
    client = discord.Client(intents=discord.Intents.default())

    @client.event
    async def on_ready():
        print(f'{client.user} is no running!')

    client.run(TOKEN)
