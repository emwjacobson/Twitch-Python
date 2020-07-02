import time
from typing import Optional, Union

from rx.subject import Subject

import twitch
import twitch.chat as chat


class Chat(Subject):

    def __init__(self, channel: Union[str, list], nickname: str, oauth: str, capture_commands: bool = False, helix: Optional['twitch.Helix'] = None):
        """
        :param channel: Channel name
        :param nickname: User nickname
        :param oauth: Twitch OAuth
        :param helix: Optional Helix API
        """
        super().__init__()
        self.helix: Optional['twitch.Helix'] = helix

        self.capture_commands = capture_commands

        self.irc = chat.IRC(nickname, password=oauth, capture_commands=self.capture_commands)
        self.irc.incoming.subscribe(self._message_handler)
        self.irc.start()

        self.channel = channel
        self.joined: bool = False

    def _message_handler(self, data: bytes) -> None:
        # First messages are server connection messages,
        # which should be handled by joining the chat room.
        if not self.joined:
            if isinstance(self.channel, str):
                self.irc.join_channel(self.channel)
                self.joined = True
            elif isinstance(self.channel, list):
                for chan in self.channel:
                    self.irc.join_channel(chan)
                self.joined = True

        text = data.decode("UTF-8").strip('\n\r')

        # Handler for normal chat messages, send via PRIVMSG
        if text.find('PRIVMSG') >= 0:
            c = text.split(' PRIVMSG ', 1)[1].split()[0].lstrip('#')

            s = text.split(' ', 1)
            tags = s[0][1:].split(';')
            msg = s[1]

            t = {}
            for tag in tags:
                i, d = tag.split('=')
                t[i] = d

            sender = msg.split('!', 1)[0][1:]
            message = msg.split('PRIVMSG', 1)[1].split(':', 1)[1]

            self.on_next(
                chat.Message(message_type=chat.MessageType.CHAT, channel=c, sender=sender, text=message, tags=t, helix_api=self.helix, chat=self, raw=text)
            )
        # Handles chat commands if capture_commands is True
        elif self.capture_commands and ':tmi.twitch.tv' in text:
            tags, cmd = text.split(":tmi.twitch.tv", 1)
            args = cmd.strip().split(" ")

            cmd_type = None
            msg = None
            if args[0] == "CLEARCHAT":
                cmd_type = chat.CommandType.CLEARCHAT
                if len(args) >= 3:
                    msg = args[2][1:]
            elif args[0] == "CLEARMSG":
                cmd_type = chat.CommandType.CLEARMSG
                if len(args) >= 3:
                    msg = args[2][1:]
            elif args[0] == "HOSTTARGET":
                cmd_type = chat.CommandType.HOSTTARGET
                if len(args) >= 3:
                    msg = " ".join(args[2])[1:]
            elif args[0] == "NOTICE":
                cmd_type = chat.CommandType.NOTICE
                msg = " ".join(args[2:])[1:]
            elif args[0] == "RECONNECT":
                cmd_type = chat.CommandType.RECONNECT
            elif args[0] == "ROOMSTATE":
                cmd_type = chat.CommandType.ROOMSTATE
            elif args[0] == "USERNOTICE":
                cmd_type = chat.CommandType.USERNOTICE
                if len(args) >= 3:
                    msg = " ".join(args[2:])[1:]
            elif args[0] == "USERSTATE":
                cmd_type = chat.CommandType.USERSTATE
            else:
                # print("Command else", text)
                return

            c = args[1].lstrip('#')

            t = {}
            for tag in tags[1:].split(';'):
                i, d = tag.split('=')
                t[i] = d

            self.on_next(
                chat.Message(message_type=chat.MessageType.COMMAND, channel=c, sender=None, text=msg, tags=t, helix_api=self.helix, chat=self, command_type=cmd_type, raw=text)
            )
        # else:
        #     print("Outside else", text)

    def send(self, message: str) -> None:
        while not self.joined:
            time.sleep(0.01)
        self.irc.send_message(message=message, channel=self.channel)

    def __del__(self):
        self.irc.active = False
        self.dispose()
