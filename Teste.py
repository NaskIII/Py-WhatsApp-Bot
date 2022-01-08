from core import Whatsapp
import time


whats = Whatsapp.Whatsapp_API()
whats.web(5)
whats.contacts('Teste para a Cortana')
whats.message('Olá, sou Cortana, é um prazer ver vocês.')
whats.send_message()
while True:
    message: str = whats.read_message('!')
    if message == '!ping':
        whats.answer_message('pong')
        time.sleep(60)
    if message == '!pong':
        whats.answer_message('ping')
        time.sleep(60)
    if message == '!quit':
        whats.answer_message('Adeus!')
        whats.quit()
        time.sleep(60)
    if message == '!image':
        print('starting')
        whats.read_image()
        time.sleep(60)