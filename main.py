import random
import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
bot = commands.Bot(command_prefix='!', intents=intents)

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
            await interaction.response.send_message('พิมพ์คำสั่งเองดีน่อง!', ephemeral= True)
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

class XoView(discord.ui.View):
    def __init__(self, player_x: discord.User, player_o: discord.User):
        super().__init__(timeout=300)
        self.player_x = player_x
        self.player_o = player_o
        self.board = ["-"] * 9
        self.current_turn = player_x

        async def on_timeout(self):
            for item in self.children:
                item.disabled = True

    def make_callback(self, index):
        async def button_callback(interaction: discord.Interaction):
            if interaction.user != self.current_turn:
                await interaction.response.send_message('ยังไม่ถึงตามึ..คุณ', ephemeral=True)
                return

            if self.board[index] != "-":
                await interaction.response.send_message('อย่ามากดซ้ำ', ephemeral=True)
                return

            symbol = "❌" if self.current_turn == self.player_x else "⭕"
            self.board[index] = symbol

            for child in self.children:
                if isinstance(child, discord.ui.Button) and child.custom_id == f"xo_{index}":
                    child.label=symbol
                    child.style=discord.ButtonStyle.green
                    child.disabled=True
                    break

            if await self.win_check(interaction):
                return
            
            self.current_turn = self.player_o if self.current_turn == self.player_x else self.player_x

            await interaction.response.edit_message(
                content=f'ตากูอ้าาา!ไม่นะ ตาของ **{self.current_turn.display_name}**',
                view=self
            )

        return button_callback

    async def win_check(self, interaction: discord.Interaction):
        wins = [
            (0, 1, 2),(3, 4, 5),(6, 7, 8),
            (0, 3, 6),(1, 4, 7),(2, 5, 8),
            (0, 4, 8),(2, 4, 6),
        ]

        for a, b, c in wins:
            if self.board[a] == self.board[b] == self.board[c] != "-":
                winner_symbol = self.board[a]
                winner = self.player_x if winner_symbol == "❌" else self.player_o

                for child in self.children:
                    if isinstance(child, discord.ui.Button) and child.custom_id is not None:
                        child.disabled = True
                
                await interaction.response.edit_message(
                    content=f'ใครหนอชนะ?อ๋อ **{winner.display_name}** เองจร้า',
                    view=None
                )
                return True

        if "-" not in self.board:
                await interaction.response.edit_message(
                    content='จบล่ะโห่เสมอกันกากทั้งคู่',
                view=None
                )
                return True
    
        return False

    @discord.ui.button(label='เข้าร่วมเกม', style=discord.ButtonStyle.green, custom_id='join')
    async def join_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user == self.player_x:
            await interaction.response.send_message('คุณมึงเป็นคนเปิดเกมโว้ยย!', ephemeral=True)
            return

        self.player_o = interaction.user
        self.remove_item(button)

        for i in range(9):
            button = discord.ui.Button(
                label="-",
                style=discord.ButtonStyle.gray,
                row=i // 3,
                custom_id=f"{i}"
            )
            button.callback = self.make_callback(i)
            self.add_item(button)

        await interaction.response.edit_message(
            content=f'เกมเริ่มแล้วตอนนี้ตา **{self.player_x.display_name}** เล่นกับ **{self.player_o.display_name}**',
            view=self
        )

@bot.tree.command(name="ping", description='Replies with Pong!')
async def slash_ping(interaction: discord.Interaction):
    await interaction.response.send_message('pong!')

@bot.tree.command(name="rps", description='Play Rock, Paper, Scissors!')
async def slash_rps (interaction: discord.Interaction):
    view = RPSView(interaction.user)
    await interaction.response.send_message('เลือก ค้อน,กระดาษ,กรรไกร', view=view)

@bot.tree.command(name='xo', description='เล่นเกม XO!')
async def slash_xo(interaction: discord.Interaction):
    view = XoView(player_x=interaction.user, player_o=None)
    await interaction.response.send_message(f'{interaction.user.mention} เปิดเกม XO! ใครก็ได้มาเล่นด้วยหน่อย', view=view)

if __name__ == "__main__":
    if not TOKEN:
        raise ValueError('No DISCORD_TOKEN found in .env file.')
    bot.run(TOKEN)
