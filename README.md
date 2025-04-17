# peacekeeper

discord bot

"I keep the peace. If the monitored users spam a certain amount of messages within a given time frame, I will spam animal gifs.
"

Currently hosted on Replit

## Installation
1. `pip install discord.py aiohttp python-dotenv`
2. `python peacekeeper.py`

## Env Variables
- `MONITORED_USERS` - Comma-separated list of Discord user IDs to monitor for spam.
- `MESSAGE_LIMIT` - The number of messages a monitored user can send within the time window before being considered spam.
- `TIME_WINDOW` - The time window in seconds for monitoring the message limit.
- `SPAM_AMOUNT` - The number of gifs to send when spam is detected.
- `MINIMUM_MESSAGE_PER_USER` - The minimum number of messages a monitored user must send to be considered for spam detection.
- `MONITORED_CHANNEL_ID` - The ID of the channel to monitor for spam.
- `TENOR_API_KEY` - Your Tenor API key for fetching gifs.
- `DISCORD_BOT_TOKEN` - The Discord bot token.


Created by Lina on 2025-04-17