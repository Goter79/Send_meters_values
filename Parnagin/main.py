import json
import telebot;
from telebot.types import  ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from database import Database
from config import TOKEN;

database = Database()

bot = telebot.TeleBot(TOKEN)

@bot.callback_query_handler(func=lambda call:True)
def callback_query(call):
    req = call.data.split('_')

    if req[0] == 'unseen':
        bot.delete_message(call.message.chat.id, call.message.message_id)
    elif 'pagination' in req[0]:
        json_string = json.loads(req[0])
        count = json_string['CountPage']
        page = json_string['NumberPage']

## переделать класс обработки данных из таблицы
## в запрос передавать номер ЛС и текущий id_meter с сортировкой по Service+id_meter c порядковым номером
## в InlineKeyboardButton, в callback_data передавать id_meter 
## <- Назад     2/100      Вперед->
##   231         232        233
## первый массив из таблицы - данные по mid id_meter
## второй массив это start mid end  - айдишники ИПУ относительно текущего ИПУ с сортировкой (LS+Service+id_meter)
## как то написать запрос который вернет эти данные

        sqlTransaction = database.listColledjeForPage(tables='organization', order='title', Page=page,
                                                      SkipSize=1)  # SkipSize - т.к я буду отображать по одной записи
        data = sqlTransaction[0][0]
        count = sqlTransaction[2]

        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton(text='Скрыть', callback_data='unseen'))
        if page == 1:
            markup.add(InlineKeyboardButton(text=f'{page}/{count}', callback_data=f' '),
                       InlineKeyboardButton(text=f'Вперёд --->',
                                            callback_data="{\"method\":\"pagination\",\"NumberPage\":" + str(
                                                page + 1) + ",\"CountPage\":" + str(count) + "}"))
        elif page == count:
            markup.add(InlineKeyboardButton(text=f'<--- Назад',
                                            callback_data="{\"method\":\"pagination\",\"NumberPage\":" + str(
                                                page - 1) + ",\"CountPage\":" + str(count) + "}"),
                       InlineKeyboardButton(text=f'{page}/{count}', callback_data=f' '))
        else:
            markup.add(InlineKeyboardButton(text=f'<--- Назад', callback_data="{\"method\":\"pagination\",\"NumberPage\":" + str(page-1) + ",\"CountPage\":" + str(count) + "}"),
                           InlineKeyboardButton(text=f'{page}/{count}', callback_data=f' '),
                           InlineKeyboardButton(text=f'Вперёд --->', callback_data="{\"method\":\"pagination\",\"NumberPage\":" + str(page+1) + ",\"CountPage\":" + str(count) + "}"))
        bot.edit_message_text(f'<b>{data[3]}</b>\n\n'
                                    f'<b>Короткое название:</b> <i>{data[4]}</i>\n'
                                    f'<b>Email:</b><i>{data[6]}</i>\n'
                                    f'<b>Сайт:</b><i> {data[8]}</i>',
                                    parse_mode="HTML",reply_markup = markup, chat_id=call.message.chat.id, message_id=call.message.message_id)


@bot.message_handler(content_types=['text'])
def start(m):
    page = 1
    sqlTransaction = database.listColledjeForPage(tables = 'organization', order='title', Page=page, SkipSize=1) # SkipSize - т.к я буду отображать по одной записи
    data = sqlTransaction[0][0]  # Набор строк
    count = sqlTransaction[2]  # Количество строк
    print()
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(text='Скрыть', callback_data='unseen'))
    markup.add(InlineKeyboardButton(text=f'{page}/{count}', callback_data=f' '),
               InlineKeyboardButton(text=f'Вперёд --->', callback_data="{\"method\":\"pagination\",\"NumberPage\":" + str(page+1) + ",\"CountPage\":" + str(count) + "}"))

    bot.send_message(m.from_user.id, f'<b>{data[3]}</b>\n\n'
                                    f'<b>Короткое название:</b> <i>{data[4]}</i>\n'
                                    f'<b>Email:</b><i>{data[6]}</i>\n'
                                    f'<b>Сайт:</b><i> {data[8]}</i>',
                     parse_mode="HTML", reply_markup = markup)


if __name__ == '__main__':
    bot.polling(none_stop=True)