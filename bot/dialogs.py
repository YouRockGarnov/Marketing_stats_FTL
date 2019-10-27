from bot.google_analitcs import get_report
from bot.models.message import Message


def register_dialog_and_message_handlers(bot):
    # @bot.dialog_handler('[Пп]олучить отчёт')
    # def default_handler(message: Message):
    #     bot.send_message(
    #         message.from_user.id, 'Error. Not a valid key'
    #     )
    #
    #     while True:
    #         message = yield from bot.get_expected_message("Hello")
    #
    #         print("hello")
    #         break

    @bot.dialog_handler('[Зз]апланировать отчёт')
    def _(message: Message):
        bot.send_message(
            message.from_user.id, 'Запланировать единоразовую отправку или '
        )

        while True:
            message = yield from bot.get_expected_message("Hello")

            print("hello")
            break

    @bot.message_handler('[Пп]олучить отчёт')
    def _(message: Message):
        dataframe = get_report()

        dataframe.to_excel(f'report{message.from_user.id}.xlsx')
        bot.send_file(
            message.from_user.id, f'report{message.from_user.id}.xlsx'
        )

        while True:
            message = yield from bot.get_expected_message("Hello")

            print("hello")
            break

    @bot.message_handler("[Hh]elp|[Пп]омощь")
    def _(message: Message):
        bot.send_message(
            message.from_user.id,
            f'Бот умеет получать отчёты из google аналитик и их планировать.'
            f'Команды:'
            f'  Запланировать отчёт'
            f'  Получить отчё'
        )

    @bot.message_handler()
    def default_handler(message: Message):
        bot.send_message(
            message.from_user.id, f'Не понял что вы хотите сделать. Напишиите "Help" или помощь"Помощь"'
        )
