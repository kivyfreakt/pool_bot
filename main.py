""" Главный файл для бота """

import telebot
from config import TOKEN_API, ADMIN
from survey.questions import QUESTIONS
from survey.texts import INTRO_TEXT, OUTRO_TEXT, START, RESTART, HELP
from models.user import Users
from models.response import Responses
from load import database

QUESTIONS_NUM = len(QUESTIONS)


def markup_choices(choices):
    """ Создание клавиатуры с ответами """
    if not choices:
        return telebot.types.ReplyKeyboardRemove(selective=False)

    markup = telebot.types.ReplyKeyboardMarkup(True, False)
    for choice in choices:
        markup.add(telebot.types.KeyboardButton(choice))

    return markup


def main():
    """ Главная функция """

    bot = telebot.TeleBot(TOKEN_API, num_threads=5)
    database.connect()
    Users.create_table()
    Responses.create_table()

    @bot.message_handler(commands=['start'])
    def send_welcome(message):
        """ Приветственная функция """

        welcome_user = "Здравствуйте " + message.from_user.first_name + \
            " " + message.from_user.last_name + INTRO_TEXT
        bot.send_message(message.chat.id, welcome_user,
                         reply_markup=markup_choices([START]))

    @bot.message_handler(commands=['stats'])
    def send_stats(message):
        """ Функция получения статистики """
        if message.from_user.id == ADMIN:
            bot.send_message(message.chat.id, "Hello, admin!")

    @bot.message_handler(commands=['help'])
    def send_help(message):
        """ Получение справки о боте """
        bot.send_message(message.chat.id, HELP)

    @bot.message_handler(content_types=['text'])
    def message_handler(message):
        """ Обработчик текста """
        user, _ = Users.get_or_create(
            user_id=message.from_user.id,
            defaults={
                "first_name": message.from_user.first_name or "",
                "last_name": message.from_user.last_name or "",
                "username": message.from_user.username or "",
            }
        )

        response = user.responses.filter(completed=False)

        if response:
            response = response[0]  # ????

        if not response and message.text in [START, RESTART]:
            response = Responses(details={}, user=user)

        if not response:
            return

        if QUESTIONS_NUM - 1 >= response.step >= 0:
            if message.text in QUESTIONS[response.step]["choices"]:
                prev_question = QUESTIONS[response.step]["text"]
                response.details[prev_question] = message.text
                response.step += 1
                response.save()

        if response.step == QUESTIONS_NUM:
            response.completed = True
            response.save()

            bot.send_message(user.user_id, OUTRO_TEXT,
                             reply_markup=markup_choices([RESTART]))
            return

        question = QUESTIONS[response.step]
        text = question["text"]
        choices = question.get("choices") or []

        bot.send_message(user.user_id, text,
                         reply_markup=markup_choices(choices))

        # response.step += 1
        response.save()

    bot.infinity_polling()


if __name__ == '__main__':
    main()
