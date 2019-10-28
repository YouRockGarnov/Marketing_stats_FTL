from unittest.mock import MagicMock

from bot.bot import Bot


class TestBot(Bot):
    def __init__(self):
        super().__init__('test_bot')

    send_message = MagicMock()
    send_file = MagicMock()

    def run(self):
        pass
