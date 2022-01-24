# Beta Version 0.7 by Nask
# Beta version 0.7
#
# Version prepared to deal with scenarios designed for testing, where basic WhatsApp functions can be performed, such as:
#
# Receive messages from multiple chats
# Send messages to multiple chats
# Send images to multiple chats
# Receive images from multiple chats
# Send emojis to a contact or the search bar
# Turn images into stickers
# Send links
# Send files
# Who sent the message
# When they sent the message

# This version is not production ready!

from datetime import datetime


class Message(object):
    def __init__(self, message_sender: str, message_date: str, message_hour: str, message: str) -> None:
        super().__init__()
        self.message_sender: str = message_sender
        self.message_date: datetime.date = datetime.strptime(
            message_date, '%d/%m/%Y').date()
        self.message_hour: datetime.time = datetime.strptime(
            message_hour, '%H:%M').time()
        self.message: str = message
