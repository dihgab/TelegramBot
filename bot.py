import requests
import time
import json
import os


class TelegramBot:
    def __init__(self):
        token = '1800726997:AAHlFp8Avc5bLJGWnWzasYtDXJMYlbs6efU'
        self.url_base = f'https://api.telegram.org/bot{token}/'

    def Iniciar(self):
        update_id = None
        while True:
            atualizacao = self.obter_novas_mensagens(update_id)
            dados = atualizacao["result"]
            if dados:
                for dado in dados:
                    update_id = dado['update_id']
                    mensagem = str(dado["message"]["text"])
                    chat_id = dado["message"]["from"]["id"]
                    eh_primeira_mensagem = int(
                        dado["message"]["message_id"]) == 1
                    resposta = self.criar_resposta(
                        mensagem, eh_primeira_mensagem)
                    self.responder(resposta, chat_id)

    # Obter mensagens
    def obter_novas_mensagens(self, update_id):
        link_requisicao = f'{self.url_base}getUpdates?timeout=100'
        if update_id:
            link_requisicao = f'{link_requisicao}&offset={update_id + 1}'
        resultado = requests.get(link_requisicao)
        return json.loads(resultado.content)

    # Criar uma resposta
    def criar_resposta(self, mensagem, eh_primeira_mensagem):
        if eh_primeira_mensagem == True or mensagem in ('menu', 'Menu'):
            return f'''OK!{os.linesep}Digite o número do que deseja experimentar:{os.linesep}1 - Empada{os.linesep}2 - Doce{os.linesep}3 - Bolo{os.linesep}{os.linesep}Com os comprimentos de Diego Gabriel.'''
        if mensagem == '1':
            return f'''Empada - R$5,00(10 unidades){os.linesep}Deseja confirmar o pedido?(sim/não)
            '''
        elif mensagem == '2':
            return f'''Doce - R$10,00{os.linesep}Deseja confirmar o pedido? (sim/não)
            '''
        elif mensagem == '3':
            return f'''Bolo - R$20,00(Chocolate){os.linesep}Deseja confirmar o pedido?(sim/não)'''

        elif mensagem.lower() in ('s', 'sim'):
            return f''' Pedido Confirmado!{os.linesep}Tenha um bom apetite. '''
        elif mensagem.lower() in ('n', 'não'):
            return f''' Certo, volte ao menu se quiser experimentar outros pedidos. '''

        elif mensagem.lower() in ('teste', 'testando'):
            return f''' Recalibração concluída. '''
            
        else:
            return f'''Em quê posso ajuda-lo?{os.linesep}No momento minha única funcionalidade é servi-lo{os.linesep}Digite "menu" para conferir o cardápio. :)'''

    # Responder
    def responder(self, resposta, chat_id):
        link_requisicao = f'{self.url_base}sendMessage?chat_id={chat_id}&text={resposta}'
        requests.get(link_requisicao)


bot = TelegramBot()
bot.Iniciar()
