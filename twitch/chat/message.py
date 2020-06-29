from typing import Optional
from enum import Enum

from twitch.helix import User, Helix
from .chat import Chat

class MessageType(Enum):
    CHAT = 1
    COMMAND = 2

class CommandType(Enum):
    CLEARCHAT = 1
    CLEARMSG = 2
    HOSTTARGET = 3
    NOTICE = 4
    RECONNECT = 5
    ROOMSTATE = 6
    USERNOTICE = 7
    USERSTATE = 8

class Message:

    def __init__(self,
                 message_type: MessageType,
                 channel: str,
                 sender: str,
                 text: str,
                 tags: dict,
                 helix_api: Optional[Helix] = None,
                 chat: Optional[Chat] = None,
                 command_type: Optional[CommandType] = None):
        self.message_type: MessageType = message_type
        self.channel: str = channel
        self.sender: str = sender
        self.text: str = text
        self.tags: dict = tags
        self.helix: Optional[Helix] = helix_api
        self.chat: Optional[Chat] = chat
        self.command_type: Optional[CommandType] = command_type

    @property
    def user(self) -> Optional[User]:
        return self.helix.user(self.sender) if self.helix else None
