""" Главный файл для бота """

import telebot
import pandas as pd
from config import TOKEN_API, ADMIN
from survey.questions import QUESTIONS, QUESTIONS_NUM
from survey.texts import INTRO_TEXT, OUTRO_TEXT, START, RESTART, HELP, STATS
from models.user import Users
from models.response import Responses, get_answers
from load import database


def markup_choices(choices):
    """ Создание клавиатуры с ответами """
    if not choices:
        return telebot.types.ReplyKeyboardRemove(selective=False)

    markup = telebot.types.ReplyKeyboardMarkup(True, False)
    for choice in choices:
        markup.add(telebot.types.KeyboardButton(choice))

    return markup


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
        data = get_answers()

        dataframe = pd.DataFrame.from_dict(data)
        dataframe.to_csv("report.csv", index=False)

        dataframe2 = dataframe.apply(pd.value_counts)

        pie = dataframe2.plot(kind='pie', subplots=True,
                                autopct = (lambda p: f'{p:.2f}%' if p > 0 else ''),
                                startangle=90, layout=(1, QUESTIONS_NUM),
                                figsize=(5*QUESTIONS_NUM, 5))

        fig = pie[0][0].get_figure()
        fig.savefig("plot.png")

        bot.send_message(message.chat.id, STATS)
        with open('plot.png', 'rb') as plot:
            bot.send_document(message.chat.id, plot)
        with open('report.csv', 'rb') as doc:
            bot.send_document(message.chat.id, doc)

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
            response.details[response.step] = message.text
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

    response.save()

bot.infinity_polling()
