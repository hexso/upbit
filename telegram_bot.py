import telegram
from telegram.ext import Updater, CommandHandler

class TelegramBot:

    def __init__(self):
        self.core = None
        self.updater = None
        self.id = None

    def SetChatId(self, chat_id):
        self.id = chat_id

    def SetToken(self, token):
        self.core = telegram.Bot(token)
        self.updater = Updater(token)

    def SendMsg(self, text):
        self.core.sendMessage(chat_id=self.id, text=text)


if __name__ == '__main__':
    #tlgBot = TelegramBot()
    with open('private.txt', 'r') as f:
        data = f.read()
        data = data.split('\n')
        for i in data:
            if 'telegramtoken' in i:
                token = i[i.find(':') + 1:]
            elif 'telegramchatid' in i:
                chatid = i[i.find(':') + 1:]
    tgBot = TelegramBot()
    tgBot.SetChatId(chatid)
    tgBot.SetToken(token)
    tgBot.SendMsg('a')
    #tlgBot.SendMsg('hello_world')
