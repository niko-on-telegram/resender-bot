import logging.config
from pathlib import Path

from telethon import TelegramClient, events

from aiogram import Bot

import logging_setup
from config_reader import config


def main():
    Path("logs").mkdir(exist_ok=True)
    logging_config = logging_setup.get_logging_config("resenderbot")
    logging.config.dictConfig(logging_config)
    bot = Bot(config.BOT_TOKEN.get_secret_value())

    logging.info(f"Setting admins to: {config.ADMINS_ID}")

    with TelegramClient('resender', config.API_ID, config.API_HASH) as client:
        @client.on(events.NewMessage(outgoing=False))
        async def handler(event: events.NewMessage.Event):
            logging.info(event)
            logging.info(event.chat_id)
            logging.info(f"event.chat_id == config.GROUP_ID = {event.chat_id == config.GROUP_ID}")

            if event.chat_id == config.GROUP_ID and event.message.text:
                for admin in config.ADMINS_ID:
                    await bot.send_message(admin, event.message.text)

        client.run_until_disconnected()


if __name__ == '__main__':
    main()
