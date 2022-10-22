import telebot
from config import token_api  # todo: fix
from survey.questions import QUESTIONS
from survey.texts import INTRO_TEXT, OUTRO_TEXT, START, RESTART
from models.user import Users
from models.response import Responses
from load import database

QUESTIONS_NUM = len(QUESTIONS)

# todo: move
def markup_choices(choices):
    if not choices:
        return telebot.types.ReplyKeyboardRemove(selective=False)

    markup = telebot.types.ReplyKeyboardMarkup(True, False)
    for choice in choices:
        markup.add(telebot.types.KeyboardButton(choice))

    return markup


def main():
    ''' 
        Главная функция
    '''

    bot = telebot.TeleBot(token_api, num_threads=5)
    database.connect()
    Users.create_table()
    Responses.create_table()

    @bot.message_handler(content_types=['text'])
    def message_handler(message):
        '''
            Обработчик текста
        '''
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
            response = response[0] # ????

        if not response or message.text in [START, RESTART]:
            response = Responses(details = {}, user = user)

        if QUESTIONS_NUM >= response.step >= 1:
            prev_question = QUESTIONS[response.step - 1]["text"]
            response.details[prev_question] = message.text
            response.save()

        if response.step >= QUESTIONS_NUM:
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

        response.step += 1
        response.save()


    @bot.message_handler(commands=['start'])
    def send_welcome(message):
        ''' 
            Приветственная функция
        '''

        welcome_user = f'Здравствуйте {message.from_user.first_name} {message.from_user.last_name}' + INTRO_TEXT
        bot.send_message(message.chat.id, welcome_user)


    try:
        bot.infinity_polling()
    except Exception as e:
        print(e)


if __name__ == '__main__':
    main()
