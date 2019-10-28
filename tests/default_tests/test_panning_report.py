def test_planing_one_reporting(bot, message_fabric, user):
    bot.handle_new_message(message_fabric('Запланировать отчёт'))

    bot.send_message.assert_called_with(user.id, 'Запланировать единоразовую отправку или периодическую.')

    bot.handle_new_message(message_fabric('Единоразовую'))

    bot.send_message.assert_called_with(user.id,
                                        'Окей, на какую дату сформировать и отправить отчёт? Укажите дату в формате '
                                        '"дд:мм:гггг чч:мм:cc"')

    # Try to send invalid datetime
    bot.handle_new_message(message_fabric('1:08:1999'))
    # Check validation
    bot.send_message.assert_called_with(user.id,
                                        'Вы ввели дату не веного формата. Введите дату в формате "дд:мм:гггг чч:мм:cc" '
                                        'или "Завершить"')

    bot.handle_new_message(message_fabric('01:08:2020 00:00:00'))

    bot.send_message.assert_called_with(user.id,
                                        f'Отчёт запланрирован на "01:08:2020 00:00:00"')


def test_planing_periodic_reporting(bot, message_fabric, user):
    bot.handle_new_message(message_fabric('Запланировать отчёт'))

    bot.send_message.assert_called_with(user.id, 'Запланировать единоразовую отправку или периодическую.')

    bot.handle_new_message(message_fabric('Периодическую'))

    bot.send_message.assert_called_with(user.id,
                                        'Окей, на какую дату сформировать и отправить отчёт? Укажите дату в формате '
                                        '"дд:мм:гггг чч:мм:cc"')

    # Try to send invalid datetime
    bot.handle_new_message(message_fabric('1:08:1999'))
    # Check validation
    bot.send_message.assert_called_with(user.id,
                                        'Вы ввели дату не веного формата. Введите дату в формате "дд:мм:гггг чч:мм:cc" '
                                        'или "Завершить"')

    bot.handle_new_message(message_fabric('01:08:2020 00:00:00'))

    bot.send_message.assert_called_with(user.id,
                                        f'Отчёт запланрирован на "01:08:2020 00:00:00"')
