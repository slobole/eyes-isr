import os
import logging

import discord
from dotenv import load_dotenv
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

load_dotenv()

DISCORD_TOKEN = os.environ["DISCORD_TOKEN"]
DISCORD_CHANNEL_ID = int(os.environ["DISCORD_CHANNEL_ID"])
SLACK_TOKEN = os.environ["SLACK_TOKEN"]
TARGET_CHANNEL = os.environ["TARGET_CHANNEL"]

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(message)s",
)
log = logging.getLogger(__name__)

slack_client = WebClient(token=SLACK_TOKEN)
discord_client = discord.Client()


def _build_slack_text(message: discord.Message) -> str:
    """Build the plain-text payload forwarded to Slack."""
    header = f"*{message.author.display_name}*"
    parts_list = [header]

    if message.content:
        parts_list.append(message.content)

    for attachment in message.attachments:
        parts_list.append(attachment.url)

    for embed in message.embeds:
        if embed.url:
            parts_list.append(embed.url)

    return "\n".join(parts_list)


def _post_to_slack(text: str) -> None:
    try:
        slack_client.chat_postMessage(channel=TARGET_CHANNEL, text=text)
        log.info("Forwarded message to Slack %s", TARGET_CHANNEL)
    except SlackApiError as exc:
        log.error("Slack API error: %s", exc.response["error"])


@discord_client.event
async def on_ready():
    log.info("Logged in as %s (id: %s)", discord_client.user, discord_client.user.id)
    log.info("Watching Discord channel %s -> Slack %s", DISCORD_CHANNEL_ID, TARGET_CHANNEL)


@discord_client.event
async def on_message(message: discord.Message):
    if message.channel.id != DISCORD_CHANNEL_ID:
        return

    text = _build_slack_text(message)
    _post_to_slack(text)


if __name__ == "__main__":
    discord_client.run(DISCORD_TOKEN)
