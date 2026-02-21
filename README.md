# eyes-isr — Discord-to-Slack Message Router

Routes messages from a Discord channel to a Slack channel in real time.

## Setup

1. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

2. **Configure `.env`**

   | Variable             | Description                          |
   |----------------------|--------------------------------------|
   | `DISCORD_TOKEN`      | Discord user token (self-bot)        |
   | `DISCORD_CHANNEL_ID` | ID of the Discord channel to monitor |
   | `SLACK_TOKEN`        | Slack bot token (`xoxb-...`)         |
   | `TARGET_CHANNEL`     | Slack channel name (e.g. `#general`) |

3. **Run**

   ```bash
   python bot.py
   ```

The bot will log in with your Discord user token, watch the configured channel, and forward every message (including attachment URLs) to the Slack channel.
