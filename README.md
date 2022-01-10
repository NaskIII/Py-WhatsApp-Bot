# Py-WhatsApp-Bot
Py-WhatsApp-Bot is a library that allows you to automatically control various WhatsApp Web functions. In addition, the library allows you to receive messages and even images, without any manual interaction.

## Links
Documentation - **Coming Soon**

## Installation
Py-WhatsApp-Bot is not yet available on PyPi.

Py-WhatsApp-Bot officially supports python 3.10+.

### Cloning the Repository
At the moment the installation is only available through github.
#### HTTPS
`git clone https://github.com/NaskIII/Py-WhatsApp-Bot.git`

## Features
- Send messages
- Receive messages
- Send Images
- Receive images
- Switch chat when another conversation executes a command
- And more is in development

## Usage
``` python
from core import Whatsapp
import os

# Start Whatsapp Bot class
whatsapp = Whatsapp.Whatsapp_API()

# Open whatsapp web, if the login has never been done, by default you will have 120 seconds to do so
whatsapp.open_whatsapp_web()

# Search for a contact in your contact list and start a conversation
whatsapp.search_contact('Matheus Morillo')

# Write a message in whatsapp web text box
whatsapp.write_message('Hi Matheus, how are you?')

# Click on the button to send the previously written message
whatsapp.click_send_message_button()

quit: bool = True

while quit:
    # Read incoming messages that contain the activation message at the beginning of the sentence.
    message_from_matheus: str = whatsapp.read_message(trigger_message='!')

    if message_from_matheus == '!ping':
        # Write and send a message to the current conversation
        whatsapp.write_and_send_message('pong')
    elif message_from_matheus.__contains__('!image'):
        # Reads an image to the current conversation, receives the activation command and the directory where the image is located
        if whatsapp.read_image(message_from_matheus, os.getcwd() + r'/images'):
            # If the image is successfully received, a confirmation message is sent.
            whatsapp.write_and_send_message("Command executed successfully")
        else:
            # If an error occurs, an error message is sent.
            whatsapp.write_and_send_message(
                "There was an unexpected error, please try again later.")
    elif message_from_matheus.__contains__('!sendimage'):
        # Send an image to the current conversation, receive the path to the image as a parameter
        if whatsapp.send_image(message_from_matheus):
            # If the image is successfully sent, a confirmation message is sent.
            whatsapp.write_and_send_message(
                "Command executed successfully")
        else:
            # If an error occurs, an error message is sent.
            whatsapp.write_and_send_message(
                "There was an unexpected error, please try again later.")
    elif message_from_matheus == '!quit':
        whatsapp.write_and_send_message('Goodbye!')
        # Close the process
        whatsapp.quit()


```
For more examples visit our Wiki

## License
MIT. For more information please [visit](https://github.com/NaskIII/Py-WhatsApp-Bot/blob/main/LICENSE)
