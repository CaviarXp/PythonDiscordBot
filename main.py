import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True

class MeBot(commands.Bot):
    async def setup_hook(self):
        for filename in os.listdir("./Cogs"):
            if filename.endswith(".py"):
                await self.load_extension(f"Cogs.{filename[:-3]}")
                print(f"Loaded {filename[:-3]}")

        await self.tree.sync()
        print("Slash commands synced")

bot = MeBot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

if __name__ == "__main__":
    if not TOKEN:
        raise ValueError('No DISCORD_TOKEN found in .env file.')
    bot.run(TOKEN)
