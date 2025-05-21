
import telebot
import config # подключаем конфиг, чтобы взять с него токен бота
 
bot = telebot.TeleBot(config.TOKEN)

text = "<div><b>Левый столбец:</b></div>" + \
        "<div>- Пункт 1</div>" + \
        "<div>- Пункт 2</div>" + \
        "<div><b>Правый столбец:</b></div>" + \
        "<div>- Пункт 3</div>" + \
        "<div>- Пункт 4</div>"

bot.send_message(chat_id=message.chat.id, text=text, parse_mode='HTML')