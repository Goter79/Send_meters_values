from telebot import TeleBot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
# from telebot.types import types
from config import TOKEN;
# Замените TOKEN на ваш токен
bot = TeleBot(TOKEN)

Meter=[1,1,1,'1111111', 'хвс', '344232', 111, 112]
@bot.message_handler(commands=['start'])
def start(message,previous_message=None):

                                
                                text =  f'<code>Лицевой счет:       </code><b>{Meter[3]}</b>\n\n' \
                                        f'<code>Улуга:              </code><b>{Meter[4]}</b>\n' \
                                        f'<code>Номер ИПУ:          </code><b>{Meter[5]}</b>\n' \
                                        f'<code>Пред-щие показания: </code><b>{str(Meter[6])}</b>\n' \
                                        f'<code>Текущие показания:  </code><b>{str(Meter[7])}</b>', 
                                bot.send_message(chat_id=message.chat.id, text=text, parse_mode='HTML')

                                # bot.send_message(chat_id=message.chat.id, text='__Нижнее подчёркивание__', parse_mode='MarkdownV2')
                                # # text="*bold* _italic_ `fixed width font` [link](http://google.com)\.", 
                                # markdown =  f'Лицевой счет:               *{Meter[5]}*\n\n' \
                                #             f'Услуга:                     *{Meter[5]}*\n' \
                                #             f'Номер ИПУ:                  *{Meter[5]}*\n' \
                                #             f'Предыдущие показания:       *{str(Meter[6])}*\n'
                                
                                # bot.send_message(chat_id=message.chat.id, text=markdown, parse_mode="MarkdownV2")
    

# Этот хэндлер будет срабатывать на команду "/pre"

@bot.message_handler(commands=['pre'])
def process_pre_command(message):

        text='``` Предварительно отформатированный текст```\n'
        bot.send_message(chat_id=message.chat.id, text=text, parse_mode="MarkdownV2")             
    
    # text = "Левый столбец:\n" + \
    #     "  * Пункт 1\n" + \
    #     "  * Пункт 2\n\n" + \
    #     "Правый столбец:\n" + \
    #     "  * Пункт 3\n" + \
    #     "  * Пункт 4"

    # bot.send_message(chat_id=message.chat.id, text=text, parse_mode='Markdown')

    # markup = InlineKeyboardMarkup()
    # btn1 = InlineKeyboardButton("<b>Кнопка 1</b>", callback_data='btn1')
    # btn2 = InlineKeyboardButton("<i>Кнопка 2</i>", callback_data='btn2')
    # key_b = InlineKeyboardButton(text='1123 👌', callback_data='1123')    
    # markup.add(btn1, btn2, key_b)
    # bot.send_message(message.chat.id, format_text( mbold('Hello'),    mitalic('World')), reply_markup=markup, parse_mode="HTML")



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
