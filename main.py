import logging

from bot.bot import Bot
from bot.dialogs import register_dialog_and_message_handlers
from flask import Flask

app = Flask(__name__) # главное приложение

@app.route('/', methods=['GET'])
def func():
    logging.basicConfig(level=logging.DEBUG)

    bot = Bot('Marketing_stats_FTL')
    register_dialog_and_message_handlers(bot)
    bot.run()


@app.route('/ping', methods=['GET'])
def func1():
    return "ok"
