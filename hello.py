from telebot import TeleBot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
# from telebot.types import types
from config import TOKEN;
# Замените TOKEN на ваш токен
bot = TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start(message,previous_message=None):

    try: bot.delete_message(message.chat.id, previous_message.id)
    except: pass

    markup = InlineKeyboardMarkup()
    btn1 = InlineKeyboardButton("<b>Кнопка 1</b>", callback_data='btn1')
    btn2 = InlineKeyboardButton("<i>Кнопка 2</i>", callback_data='btn2')
    key_b = InlineKeyboardButton(text='1123 👌', callback_data='1123')    
    markup.add(btn1, btn2, key_b)
    bot.send_message(message.chat.id, "Выбери кнопку:", reply_markup=markup)



@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.data == 'btn1':
        bot.answer_callback_query(call.id, "Выбрана кнопка 1")
    elif call.data == 'btn2':
        bot.answer_callback_query(call.id, "Выбрана кнопка 2")

    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("Кнопка 222", callback_data="but_222"))
    markup.add(InlineKeyboardButton("<b>Кнопка 1</b>", callback_data='btn4'))
    markup.add(InlineKeyboardButton("<b>Кнопка 1</b>", callback_data='btn3'))
    bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.id, reply_markup=markup)        

    # start(call.message, previous_message=call.message)

bot.infinity_polling()
