@ -1,2 +1,76 @@
# BotDiscord
Little Discord bot/app project
Do in my free time it's good, i think (´･ω･`)

A Discord bot built with Python (discord.py) featuring prefix commands, slash commands, and an interactive Rock-Paper-Scissors mini-game using Discord UI buttons.

---

## Features

- **Slash & Prefix Commands**: / application commands
- **Interactive Rock-Paper-Scissors**: Play directly in Discord using interactive button (discord.ui.View).

---

## Commands

| Command | Type | Description |
| :--- | :--- | :--- |
| /ping | Slash Command | Checks bot responsiveness (replies with pong!). |
| /rps | Slash Command | Starts an interactive Rock-Paper-Scissors gamewith clickable buttons. |

---

## Installation


### Install Dependencies
```bash
pip install -r requirements.txt
```

Create a .env file in the root directory:
```env
DISCORD_TOKEN=YOUR_DISCORD_BOT_TOKEN_HERE
```

## Tech Stack

- **Language**: Python
- **Framework**: discord.py (v2.x)
- **Configuration**: python-dotenv