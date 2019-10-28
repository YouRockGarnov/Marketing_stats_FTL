import pytest

from bot.dialogs import DEFAULT_MESSAGE
from bot.dialogs import HELP_MESSAGE


@pytest.mark.parametrize('message_text, expected_response', [
    ('Help', HELP_MESSAGE),
    ('gvrwiusuhdfoger', DEFAULT_MESSAGE)
])
def test(bot, message, expected_response):
    bot.handle_new_message(message)

    bot.send_message.assert_called_with(
        message.from_user.id,
        expected_response
    )
