import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
bot = commands.Bot(command_prefix='>', intents=intents)

@bot.event
async def on_ready():
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} slash command(s).")

    except Exception as e:
        print(f"Failed to sync commands: {e}")
    print(f" Logged in as {bot.user.name} (ID: {bot.user.id})")
    print("Bot is ready!")

@bot.command()
async def ping(ctx):
    await ctx.send('pong!')



@bot.tree.command(name="ping", description="Replies with Pong!")
async def slash_ping(interaction: discord.Interaction):
    await interaction.response.send_message("pong!")

if __name__ == "__main__":
    if not TOKEN:
        raise ValueError("No DISCORD_TOKEN found in .env file.")
    bot.run(TOKEN)
