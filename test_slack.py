"""Quick smoke-test: sends a single message to the Slack channel
configured in .env without needing a Discord connection."""

import os
import ssl
import logging

from dotenv import load_dotenv
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

load_dotenv()

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

TEST_MESSAGE = "*test-bot*\nhello this is a test"


def main() -> None:
    try:
        response = slack_client.chat_postMessage(
            channel=TARGET_CHANNEL,
            text=TEST_MESSAGE,
        )
        log.info(
            "Message sent to %s  (ts: %s)", TARGET_CHANNEL, response["ts"]
        )
    except SlackApiError as exc:
        log.error("Slack API error: %s", exc.response["error"])
        raise


if __name__ == "__main__":
    main()
