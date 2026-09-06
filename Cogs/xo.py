import discord
from discord.ext import commands
from discord import app_commands

intents = discord.Intents.default()

class XOView(discord.ui.View):
    def __init__(self, player_x: discord.User, player_o: discord.User | None = None):
        super().__init__(timeout=300)
        self.player_x = player_x
        self.player_o = player_o
        self.board = ["-"] * 9
        self.current_turn = player_x

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
                if isinstance(child, discord.ui.Button) and child.custom_id == f"{index}":
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

        if self.player_o is None:
            return False

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

class XOGame(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='xo', description='Play XO!')
    async def slash_xo(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            f'{interaction.user.display_name} เปิดเกม XO! ใครก็ได้มาเล่นด้วยหน่อย',
            view=XOView(player_x=interaction.user)
        )

async def setup(bot):
    await bot.add_cog(XOGame(bot))
