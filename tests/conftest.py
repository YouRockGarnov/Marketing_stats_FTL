import pytest

from bot.dialogs import register_dialog_and_message_handlers
from bot.models.message import Message
from bot.models.user import User
from tests.helpers import TestBot


@pytest.fixture
def user():
    return User(id=1)


@pytest.fixture
def message(user, message_text):
    return Message(user, message_text)


@pytest.fixture
def bot():
    bot = TestBot()
    register_dialog_and_message_handlers(bot)

    return bot
