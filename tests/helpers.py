from unittest.mock import MagicMock

from bot.bot import Bot


class TestBot(Bot):
    def __init__(self):
        super().__init__('test')

    send_message = MagicMock()

    def run(self):
        pass
