import random
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

class RPSView(discord.ui.View):
    def __init__(self, user):
        super().__init__(timeout=30)
        self.user = user

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user != self.user:
            await interaction.response.send_message('พิมพ์คำสั่งเองดีน่อง!')
            return False
        return True

    async def game_result(self, interaction: discord.Interaction):
        botchoice = random.choice(['ค้อน', 'กระดาษ', 'กรรไกร'])
        userchoice = interaction.data['custom_id']
        if userchoice == botchoice:
            result = "มันเป็นผลเสมอ!"
        elif (userchoice == 'ค้อน' and botchoice == 'กรรไกร') or \
             (userchoice == 'กระดาษ' and botchoice == 'ค้อน') or \
                (userchoice == 'กรรไกร' and botchoice == 'กระดาษ'):
            result = "เก่งๆชนะ!"
        else:
            result = "โหลยโท้ยแพ้บอท!"

        await interaction.message.edit(view=None, content=f"บอทเลือก {botchoice} ยูเลือก {userchoice} {result}")
        self.stop()

    @discord.ui.button(label='ค้อน', style=discord.ButtonStyle.green, custom_id='ค้อน')
    async def rock_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.game_result(interaction)

    @discord.ui.button(label='กระดาษ', style=discord.ButtonStyle.green, custom_id='กระดาษ')
    async def paper_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.game_result(interaction)

    @discord.ui.button(label='กรรไกร', style=discord.ButtonStyle.green, custom_id='กรรไกร')
    async def scissors_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.game_result(interaction)

@bot.tree.command(name="ping", description="Replies with Pong!")
async def slash_ping(interaction: discord.Interaction):
    await interaction.response.send_message("pong!")

@bot.tree.command(name="rps", description="Play Rock, Paper, Scissors!")
async def slash_rps (interaction: discord.Interaction):
    view = RPSView(interaction.user)
    await interaction.response.send_message("เลือก ค้อน,กระดาษ,กรรไกร", view=view)

if __name__ == "__main__":
    if not TOKEN:
        raise ValueError("No DISCORD_TOKEN found in .env file.")
    bot.run(TOKEN)
