import logging
import re
import typing
from os import getenv
from typing import Dict
from typing import Generator

import grpc
from dialog_api.messaging_pb2 import UpdateMessage
from dialog_api.peers_pb2 import Peer
from dialog_bot_sdk.bot import DialogBot

from bot.extractors import extract_message
from bot.models.message import Message


class Bot:
    def __init__(self, name: str, log_level=None):
        self.name = name
        self._log = logging.getLogger(f'\tBot:{self.name}\t')

        if log_level is not None:
            self._log.level = log_level

        self._bot = DialogBot.get_secure_bot(
            getenv('BOT_ENDPOINT', 'hackathon-mob.transmit.im'),  # bot endpoint from environment
            grpc.ssl_channel_credentials(),  # SSL credentials (empty by default!)
            getenv('BOT_TOKEN', '28a9a67267691d886fa571fdf051514fdeb6604a')  # bot token from environment
        )
        self._handlers = []
        self._peers: Dict[int, Peer] = {}
        self._current_dialogs: Dict[int, Generator] = {}

    def message_handler(self, regexpr=''):
        def decorator(func):
            self._handlers.append((regexpr, func))
            return func

        return decorator

    def dialog_handler(self, regexpr=''):
        def decorator(func):
            self._handlers.append((regexpr, func))
            return func

        return decorator

    def send_message(self, user_id: int, text: str):
        self._bot.messaging.send_message(self._peers[user_id], text)

    def send_file(self, user_id, path_to_file: str):
        self._bot.messaging.send_file(self._peers[user_id], path_to_file)

    def get_expected_message(self, expected_text_pattern):
        while True:
            message = yield
            if re.match(expected_text_pattern, message.text):
                return message
            elif message.text.lower() == 'завершить':
                self.send_message(message.from_user.id, 'Диалог завершён')
            else:
                self.send_message(message.from_user.id,
                                  f'Напишите то что удовлетворяет "{expected_text_pattern}" '
                                  f'или "Завершить"')

    def _find_message_handler(self, message: Message):
        if message.from_user.id in self._current_dialogs:
            try:
                self._current_dialogs[message.from_user.id].send(message)
            except StopIteration:
                del self._current_dialogs[message.from_user.id]
        else:
            for regexp, handler in self._handlers:
                if not regexp or re.match(regexp, message.text):
                    return handler

    def handle_new_message(self, message: Message):
        self._log.debug(f'Got message from user with id:{message.from_user.id} and text: {message.text}')

        if message.from_user.id in self._current_dialogs:
            try:
                self._current_dialogs[message.from_user.id].send(message)
            except StopIteration:
                del self._current_dialogs[message.from_user.id]
        else:
            handler = self._find_message_handler(message)
            if handler is not None:
                res = handler(message)
                if isinstance(res, typing.Generator):
                    next(res)
                    self._current_dialogs[message.from_user.id] = res

    def _handle_new_incoming_message(self, message: UpdateMessage):
        self.handle_new_message(extract_message(message, self._peers))

    def run(self):
        self._bot.messaging.on_message(self._handle_new_incoming_message)
