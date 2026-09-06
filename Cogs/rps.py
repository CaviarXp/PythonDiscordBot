import random
import discord
from discord.ext import commands
from discord import app_commands

intents = discord.Intents.default()

class RPSView(discord.ui.View):
    def __init__(self, user):
        super().__init__(timeout=30)
        self.user = user

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user != self.user:
            await interaction.response.send_message("พิมพ์คำสั่งเองดีน่อง!", ephemeral=True)
            return False

        return True

    async def game_result(self, interaction: discord.Interaction, userchoice: str):
        botchoice = random.choice(["ค้อน", "กระดาษ", "กรรไกร"])

        if userchoice == botchoice:
            result = "มันเป็นผลเสมอ!"

        elif (
            (userchoice == "ค้อน" and botchoice == "กรรไกร")
            or (userchoice == "กระดาษ" and botchoice == "ค้อน")
            or (userchoice == "กรรไกร" and botchoice == "กระดาษ")
        ):
            result = "เก่งๆชนะ!"

        else:
            result = "โหลยโท้ยแพ้บอท!"

        await interaction.response.edit_message(
            content=f"บอทเลือก {botchoice} ยูเลือก {userchoice} {result}",
            view=None
        )

        self.stop()

    @discord.ui.button(label="ค้อน", style=discord.ButtonStyle.green, custom_id="ค้อน")
    async def rock_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.game_result(interaction, button.label)

    @discord.ui.button(label="กระดาษ", style=discord.ButtonStyle.green, custom_id="กระดาษ")
    async def paper_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.game_result(interaction, button.label)

    @discord.ui.button(label="กรรไกร", style=discord.ButtonStyle.green, custom_id="กรรไกร")
    async def scissors_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.game_result(interaction, button.label)

class RPSGame(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="rps", description="Play Rock, Paper, Scissors!")
    async def slash_rps(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            "เลือก ค้อน, กระดาษ, กรรไกร",
            view=RPSView(interaction.user)
        )

async def setup(bot):
    await bot.add_cog(RPSGame(bot))
