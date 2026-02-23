import discord
import logging
import os
import ssl

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

ssl_ctx = ssl.create_default_context()
ssl_ctx.check_hostname = False
ssl_ctx.verify_mode = ssl.CERT_NONE

slack_client = WebClient(token=SLACK_TOKEN, ssl=ssl_ctx)


def forward_to_slack(text: str) -> None:
    try:
        slack_client.chat_postMessage(channel=TARGET_CHANNEL, text=text)
    except SlackApiError as exc:
        log.error("Slack API error: %s", exc.response["error"])


class MessageReaderClient(discord.Client):

    async def on_ready(self):
        log.info("Logged in as %s", self.user)
        channel = self.get_channel(DISCORD_CHANNEL_ID)
        if channel is None:
            log.error("Could not find channel with ID %s", DISCORD_CHANNEL_ID)
            return
        log.info("Watching #%s → Slack %s", channel.name, TARGET_CHANNEL)

    async def on_message(self, message):
        if message.channel.id != DISCORD_CHANNEL_ID:
            return

        attachment_url_list = [a.url for a in message.attachments]
        body = message.content or ""
        if attachment_url_list:
            body = body + "\n" + "\n".join(attachment_url_list) if body else "\n".join(attachment_url_list)

        if not body:
            return

        log.info("Forwarding message from %s", message.author)
        forward_to_slack(body)


client = MessageReaderClient()
client.run(DISCORD_TOKEN)
