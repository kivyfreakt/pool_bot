'''
1. пол (мужской/женский)
2. больше ли вам 30 лет? (да/нет)
3. зарабатываете ли вы больше 60т р. в месяц?(да/нет)
4. пользуются ли члены семьи стриминговыми сервисами? (да/нет)
5. на каком устройстве чаще слушаете музыку? (телефон/компьютер)
6. слушаете ли вы подкасты (да/нет)
7. важно ли вам качество звука (да/нет)
8. читаете ли вы тексты песен (да/нет)

'''

import telebot
import sqlite3
from enum import Enum

from config import token_api
from texts import intro_text, cancel_text
import markups as mark


class States(Enum):
    START = 0
    GENDER = 1
    AGE = 2
    SALLARY = 3
    FAMILY = 4
    DEVICE = 5
    PODCASTS = 6
    QUALITY = 7
    END = 8
    ERROR = -1

state = States.START

def main():
    ''' 
        Главная функция
    '''

    bot = telebot.TeleBot(token_api)

    @bot.message_handler(commands=['start'])
    def send_welcome(message):
        ''' 
            Приветственная функция
        '''
        conn = sqlite3.connect('users.db')
        cur = conn.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS users(
           userid INT PRIMARY KEY,
           fname TEXT,
           lname TEXT);
        """)
        conn.commit()

        user_info = (f'{message.chat.id}',
                     f'{message.from_user.first_name}',
                     f'{message.from_user.last_name}')

        cur.execute("INSERT OR IGNORE INTO users VALUES(?, ?, ?);", user_info)
        conn.commit()

        welcome_user = f'Здравствуйте {message.from_user.first_name} {message.from_user.last_name}' + intro_text

        bot.send_message(message.chat.id, welcome_user,
                         reply_markup=mark.main_menu)

        state = States.START

    def start_handler(message):
        if message.text == 'Отказаться':
            bot.send_message(message.chat.id, cancel_text,reply_markup = mark.del_markup)
            return States.END
        elif message.text == 'Начать':
            bot.send_message(message.chat.id, 'Хорошо! Укажите Ваш пол.', reply_markup = mark.sex)
            return States.GENDER
        else:
            bot.send_message(message.chat.id, 'Мы Вас не понимаем.')
        return States.START
        
    def end_handler(message):
        if '!' in message.text:
            bot.send_message(
                message.chat.id, 'Спасибо за ответ, мы его сохранили!', reply_markup = mark.del_markup)
        elif message.text in ('Да', 'Нет'):
            # СОХРАНЕНИЕ ДАННЫХ В БД
            bot.send_message(
                message.chat.id, 'Спасибо за прохождениe опроса! Мы Вас любим <3', reply_markup = mark.del_markup)
        return States.END

    
    def handler(message, new_message_text, current_state, answers = ('Да', 'Нет'), keyboard_type = mark.default):
        if message.text in answers:
            # сохранение информации во временном месте
            bot.send_message(message.chat.id, new_message_text, reply_markup = keyboard_type)
            return States(current_state.value + 1)
        else:
            bot.send_message(message.chat.id, 'Мы Вас не понимаем.' + current_state.name)
        return current_state

    @bot.message_handler(content_types=['text'])
    def send_markup(message):
        '''
            Обработчик текста
        '''

        global state # ПОЛНОЕ ГОВНО ПЕРЕПИСАТЬ!!!
        
        if state == States.START:
            state = start_handler(message)
        elif state == States.END:
            state = end_handler(message)
        elif state == States.GENDER:
            state = handler(message, 'Хорошо! Укажите, больше ли вам 30 лет?', state, answers=('Мужской', 'Женский'))
        elif state == States.AGE:
            state = handler(message, 'Good! Вопрос от Юрия Дудя. Вы зарабатываете больше 60 т.р в месяц?', state)
        elif state == States.SALLARY:
            state = handler(message, 'Спасибо! Пользуются ли члены семьи стриминговыми сервисами?', state)
        elif state == States.FAMILY:
            state = handler(message, 'Круто! На каком устройстве Вы чаще слушаете музыку?', state, keyboard_type=mark.device)
        elif state == States.DEVICE:
            state = handler(message, 'Благодарим. Слушаете ли Вы подкасты?', state, answers=('Телефон', 'Компьютер'))
        elif state == States.PODCASTS:
            state = handler(message, 'Ого! Важно ли вам качество звука?', state)
        elif state == States.QUALITY:
            state = handler(message, 'Понимаем! Читаете ли вы тексты песен?', state)

    try:
        bot.infinity_polling()
    except Exception as e:
        print(e)


if __name__ == '__main__':
    main()
