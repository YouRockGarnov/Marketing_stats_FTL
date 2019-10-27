import pytest


@pytest.mark.parametrize('message_text', ['Hello'])
def test(bot, message):
    bot.handle_new_message(message)

    bot.send_message.assert_called_with(
        message.from_user.id,
        f'Command "{message.text}" not understand'
    )
