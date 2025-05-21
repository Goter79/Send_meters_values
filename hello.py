from telebot import TeleBot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
# from telebot.types import types
from config import TOKEN;
# Замените TOKEN на ваш токен
bot = TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start(message,previous_message=None):

                                text =  '<b>bold</b>, <strong>bold</strong> '  \
                                        '<i>italic</i>, <em>italic</em>'  \
                                        '<u>underline</u>, <ins>underline</ins>'  \
                                        '<s>strikethrough</s>, <strike>strikethrough</strike>, <del>strikethrough</del>'  \
                                        '<span class="tg-spoiler">spoiler</span>, <tg-spoiler>spoiler</tg-spoiler>'  \
                                        '<b>bold <i>italic bold <s>italic bold strikethrough <span class="tg-spoiler">italic bold strikethrough spoiler</span></s> <u>underline italic bold</u></i> bold</b>'  \
                                        '<a href="http://www.example.com/">inline URL</a>'  \
                                        '<a href="tg://user?id=123456789">inline mention of a user</a>'  \
                                        '<code>inline fixed-width code</code>'  \
                                        '<pre>pre-formatted fixed-width code block</pre>'  \
                                        '<pre><code class="language-python">pre-formatted fixed-width code block written in the Python programming language</code></pre>>'
                                bot.send_message(chat_id=message.chat.id, text=text, parse_mode='HTML')


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
