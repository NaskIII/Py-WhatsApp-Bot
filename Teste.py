from core import Whatsapp
import time


whats = Whatsapp.Whatsapp_API(width=1280, height=720)
whats.web(5)
whats.contacts('Teste para a Cortana')
whats.message('Olá, sou Cortana, é um prazer ver vocês.')
whats.send_message()
while True:
    message: str = whats.read_message('!')
    if message == '!ping':
        whats.answer_message('pong')
    if message == '!pong':
        whats.answer_message('ping')
    if message == '!quit':
        whats.answer_message('Adeus!')
        whats.quit()
    if message.__contains__('!image'):
        if len(message.split()) <= 1:
            whats.answer_message('Por favor, siga as regras de imagem.')
        elif len(message.split()) >= 2:
            if whats.read_image(message.split()[1], message):
                whats.answer_message("Comando executado com sucesso.")
            else:
                whats.answer_message(
                    "Houve um erro inesperado, por favor siga as regras de imagem e tende novamente mais tarde.")

