from datetime import datetime

from bot.bot import Bot
from bot.google_analitcs import get_report
from bot.models.message import Message
from bot.utils import TmpDir

DEFAULT_MESSAGE = 'Не понял что вы хотите сделать. Напишиите "Help" или помощь"Помощь"'
HELP_MESSAGE = 'Бот умеет получать отчёты из google аналитик и их планировать.\n' \
               'Команды:  \n' \
               '  Запланировать отчёт\n' \
               '  Получить отчё\n' \
               'Для добавленя вашего аккауунта обратитесь в службу поддержки.'


def register_dialog_and_message_handlers(bot: Bot):
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
            message.from_user.id, 'Запланировать единоразовую отправку или периодическую.'
        )

        message = yield from bot.get_expected_message("[Ее]диноразовую|[Пп]ериодическую")

        if message.text.lower() == 'единоразовую':
            bot.send_message(
                message.from_user.id, 'Окей, на какую дату сформировать и отправить отчёт? '
                                      'Укажите дату в формате "дд:мм:гггг чч:мм:cc"'
            )

            datetime_ = yield from bot.get_expected_datetime("%d:%m:%Y %H:%M:%S", "дд:мм:гггг чч:мм:cc")

            bot.send_message(
                message.from_user.id, f'Отчёт запланрирован на "{datetime_.strftime("%d:%m:%Y %H:%M:%S")}"'
            )

    @bot.message_handler('[Пп]олучить отчёт')
    def _(message: Message):
        bot.send_message(
            message.from_user.id, f'Начал формировать отчёт'
        )

        with TmpDir() as tmp_dir:
            path_to_file = tmp_dir / f'report{message.from_user.id}.html'

            dataframe = get_report()

            dataframe.to_html(path_to_file)
            bot.send_file(
                message.from_user.id, path_to_file
            )

    @bot.message_handler("[Hh]elp|[Пп]омощь")
    def _(message: Message):
        bot.send_message(
            message.from_user.id,
            HELP_MESSAGE
        )

    @bot.message_handler()
    def default_handler(message: Message):
        bot.send_message(
            message.from_user.id, DEFAULT_MESSAGE
        )
