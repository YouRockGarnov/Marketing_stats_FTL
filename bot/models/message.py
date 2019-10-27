from dataclasses import dataclass

from bot.models.user import User


@dataclass
class Message:
    from_user: User
    text: str
