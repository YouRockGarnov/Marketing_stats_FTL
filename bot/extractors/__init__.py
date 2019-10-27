from dialog_api.messaging_pb2 import UpdateMessage

from bot.models.message import Message
from bot.models.user import User


def extract_message(input_data: UpdateMessage, peers) -> Message:
    if input_data.peer.id not in peers:
        peers[input_data.peer.id] = input_data.peer

    return Message(
        from_user=User(input_data.peer.id),
        text=str(input_data.message.textMessage.text),
    )
