import pytest


@pytest.mark.parametrize('message_text', ['Получить отчёт'])
def test_get_report(bot, message):
    bot.handle_new_message(message)


