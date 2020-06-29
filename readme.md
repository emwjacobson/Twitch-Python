# Twitch Python

[![Discord](https://user-images.githubusercontent.com/7288322/34471967-1df7808a-efbb-11e7-9088-ed0b04151291.png)](https://discord.gg/wZJFeXC)
[![Build Status](https://api.travis-ci.org/PetterKraabol/Twitch-Python.svg?branch=master)](https://travis-ci.org/PetterKraabol/Twitch-Python)


`pip install --user twitch-python`

An object-oriented approach to accessing the Twitch API and live chat with relationships and smart caching.

### Requirements

* [Python 3.7 or newer](https://www.python.org/downloads/)
* [A Twitch client ID](https://dev.twitch.tv/console/apps)

### Usage

```python
# Twitch API

import twitch

helix = twitch.Helix('client-id')
```

```python
# Users

for user in helix.users(['sodapoppin', 'reckful', 24250859]):
    print(user.display_name)


print(helix.user('zarlach').display_name)
```

```python
# Videos

for video in helix.videos([318017128, 317650435]):
    print(video.title)


print(helix.video(318017128).title)
```

```python
# Video Comments (VOD chat)

for comment in helix.video(318017128).comments:
    print(comment.commenter.display_name)


for video, comments in helix.videos([318017128, 317650435]).comments:
    for comment in comments:
        print(comment.commenter.display_name, comment.message.body)


for video, comments in helix.user('sodapoppin').videos().comments:
        for comment in comments:
            print(comment.commenter.display_name, comment.message.body)


for user, videos in helix.users(['sodapoppin', 'reckful']).videos(first=5):
        for video, comments in videos.comments:
            for comment in comments:
                print(comment.commenter.display_name, comment.message.body)
```

```python
# Twitch Chat

def handle_message(message):
    if message.type == twitch.chat.MessageType.CHAT:
        print(message.channel, message.user.display_name, message.text)
    elif message.type == twitch.chat.MessageType.COMMAND:
        # List of commands can be found at: https://dev.twitch.tv/docs/irc/commands
        # Some commands will have tags associated with them

        # Each command can have different tags associated with it, they are stored as
        # a dict in the `tags` attribute.
        # The tags associated with each command can be found at:
        # https://dev.twitch.tv/docs/irc/tags
        if message.command_type == twitch.chat.CommandType.USERNOTICE:
            print(message.tags)

# If you would like to capture commands sent from the server, set `capture_commands`
# to true. Defaults to False.
twitch.Chat(channel='#sodapoppin', nickname='zarlach', capture_commands=True, oauth='oauth:xxxxxx').subscribe(handle_message)
```

### Features
- Object-oriented relationships
- Smart caching
- New Twitch API (Helix)
- VOD chat from Twitch API v5

---

[Documentation](https://github.com/PetterKraabol/Twitch-Python/wiki) • [Twitch API](https://dev.twitch.tv/docs/) • [Twitch-Chat-Downloader](https://github.com/PetterKraabol/Twitch-Chat-Downloader)
