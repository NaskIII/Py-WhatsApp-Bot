from core import Whatsapp


whats = Whatsapp.Whatsapp_API(width=1280, height=720)
whats.web(5)
whats.contacts('Creuza')
whats.message('Olá, sou Cortana, é um prazer ver vocês.')
whats.send_message()

quit: bool = True

while quit:
    message: str = whats.read_message('!')
    if message == '!ping':
        whats.answer_message('pong')
    if message == '!pong':
        whats.answer_message('ping')
    if message == '!quit':
        whats.answer_message('Adeus!')
        whats.quit()
        quit = False
    if message.__contains__('!image'):
        if len(message.split()) <= 1:
            whats.answer_message('Por favor, siga as regras de imagem.')
        elif len(message.split()) >= 2:
            if whats.read_image(message.split()[1], message):
                whats.answer_message("Comando executado com sucesso.")
            else:
                whats.answer_message(
                    "Houve um erro inesperado, por favor siga as regras de imagem e tente novamente mais tarde.")
    if message.__contains__('!simage'):
        if len(message.split()) <= 1:
            whats.answer_message('Por favor, siga as regras de imagem.')
        elif len(message.split()) >= 2:
            if whats.send_image(message.split('_')[1]):
                whats.answer_message("Comando executado com sucesso.")
            else:
                whats.answer_message(
                    "Houve um erro inesperado, por favor siga as regras de imagem e tende novamente mais tarde.")