# DiscordBot

A small Python Discord bot built with `discord.py`. The bot uses slash commands and keeps each command group in its own cog so new features can be added without making `main.py` messy.

## Features

- Slash commands powered by `discord.py`
- Automatic cog loading from the `Cogs` folder
- `/ping` latency check
- Rock-paper-scissors game with Discord UI buttons
- XO game with a join button and interactive board

## Commands

| Command | Description |
| --- | --- |
| `/ping` | Replies with the bot latency in milliseconds. |
| `/rps` | Starts a rock-paper-scissors game. |
| `/xo` | Starts an XO game that another user can join. |

## Setup

Install the Python dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file in the project root:

```env
DISCORD_TOKEN=your_discord_bot_token_here
```

Run the bot:

```bash
python main.py
```

## Discord Bot Settings

In the Discord Developer Portal, make sure your bot has the permissions it needs to use slash commands and send messages in your server.

If you invite the bot with OAuth2, include:

- `bot`
- `applications.commands`

## Adding New Commands

Create a new file inside `Cogs/`, define a `commands.Cog`, and add a `setup` function:

```python
async def setup(bot):
    await bot.add_cog(MyCog(bot))
```

The bot will load it automatically on startup.

## Music Status

Music/Lavalink support is currently not included in the stable bot because the YouTube plugin is bugged right now. The music work can be added later once the plugin issue is fixed.

## Tech Stack

- Python
- discord.py
- python-dotenv
