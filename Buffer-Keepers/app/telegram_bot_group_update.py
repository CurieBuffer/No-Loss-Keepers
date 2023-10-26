import asyncio
import os
from enum import Enum

import telegram


class Topics(Enum):
    EMERGENCY = 6
    GENERAL = 6688
    SF = 13414
    KEEPER = 20729


def send_message(text, topic=Topics.EMERGENCY):
    api_key = os.environ["TELEGRAM_BOT_TOKEN"]
    user_id = "-1001807634869"  # Buffer Telegram Internal Group

    bot = telegram.Bot(token=api_key)
    # run this in a separate thread
    asyncio.run(
        bot.send_message(chat_id=user_id, text=text, reply_to_message_id=topic.value)
    )


def send_photo(photo, topic):
    api_key = os.environ["TELEGRAM_BOT_TOKEN"]
    user_id = "-1001807634869"  # Buffer Telegram Internal Group

    bot = telegram.Bot(token=api_key)
    # run this in a separate thread
    asyncio.run(
        # bot.send_message(chat_id=user_id, text=text, reply_to_message_id=topic.value)
        bot.send_photo(chat_id=user_id, photo=photo, reply_to_message_id=topic.value)
    )
