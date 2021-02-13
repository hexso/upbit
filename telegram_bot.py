import telegram
from telegram.ext import Updater, CommandHandler

class TelegramBot:

    def __init__(self, token, chat_id):
        self.core = telegram.Bot(token)
        self.updater = Updater(token)
        self.id = chat_id

    def SendMsg(self, text):
        self.core.sendMessage(chat_id=self.id, text=text)


if __name__ == '__main__':
    tgBot = TelegramBot('토큰번호','채팅방ID')
    updates = tgBot.core.getUpdates()
    for u in updates:
        print(u.message)
    tgBot.SendMsg('hello_world')
