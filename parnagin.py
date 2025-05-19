# Импорты
import telebot
import sqlite3
from telebot import types
from config import TOKEN;

# Создаем экземпляр бота (создаем бота)
bot = telebot.TeleBot(TOKEN, parse_mode="MARKDOWN")


# команда /start    
@bot.message_handler(commands=['start'])
def start(message, page=1, previous_message=None):


    connect = sqlite3.connect("reports.db")
    cursor = connect.cursor()
    
    pages_count_query = cursor.execute(f"SELECT COUNT(*) FROM `Meter_Measure`  limit 10")
    pages_count = int(pages_count_query.fetchone()[0])


    product_query = cursor.execute(f"SELECT id_meter, LS, Number FROM Meter_Measure limit 10")
    title, description, photo_path = product_query.fetchone()


    # cursor.execute(f"UPDATE `users` SET `page` = ? WHERE `id` = ?;", (page,message.chat.id))
    # connect.commit()

    buttons = types.InlineKeyboardMarkup()

    left  = page-1 if page != 1 else pages_count
    right = page+1 if page != pages_count else 1


    left_button  = types.InlineKeyboardButton("←", callback_data=f'to {left}')
    page_button  = types.InlineKeyboardButton(f"{str(page)}/{str(pages_count)}", callback_data='_') 
    right_button = types.InlineKeyboardButton("→", callback_data=f'to {right}')
    buy_button   = types.InlineKeyboardButton("КУПИТЬ", callback_data='buy')
    buttons.add(left_button, page_button, right_button)
    buttons.add(buy_button)


    try: 
        try: photo = open(photo_path, 'rb')
        except: photo = photo_path
        msg  = f"Название: *{title}*\nОписание: "
        msg += f"*{description}*\n" if description != None else '_нет_\n'

        bot.send_photo(message.chat.id, photo=photo, caption=msg, reply_markup=buttons)
    except: 
        msg  = f"Название: *{title}*\nОписание: "
        msg += f"*{description}*\n" if description != None else '_нет_\n'

        # bot.send_message(message.chat.id, msg, reply_markup=buttons)
        bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.id, reply_markup=markup)        

    # try: bot.delete_message(message.chat.id, previous_message.id)
    # except: pass


# Обработчик callback
@bot.callback_query_handler(func=lambda c: True)
def callback(c):
    if 'to' in c.data: 
        page = int(c.data.split(' ')[1])
        start(c.message, page=page, previous_message=c.message)



# Запуск бота
bot.polling(none_stop=True)