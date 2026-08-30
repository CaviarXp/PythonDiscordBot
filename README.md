# DiscordBot
Little Discord app/bot project

A Discord bot built with Python (discord.py) featuring prefix commands, slash commands, mini-game using Discord UI buttons.

---

## Features

- **Slash & Prefix Commands**: / application Commands.

---

## Commands

| Command | Type | Description |
| :--- | :--- | :--- |
| /ping | Slash Command | Checks bot responsiveness (replies with pong!). |
| /rps | Slash Command | Starts Rock-Paper-Scissors game. |
| /xo | Slash Command | Starts XO game. (with anyone that click เข้าร่วม/join)|
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