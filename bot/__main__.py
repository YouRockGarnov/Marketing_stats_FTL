import logging

from bot.bot import Bot
from bot.dialogs import register_dialog_and_message_handlers

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    bot = Bot('Marketing_stats_FTL')
    register_dialog_and_message_handlers(bot)
    bot.run()
