import telebot

main_menu = telebot.types.ReplyKeyboardMarkup(True)
main_menu.row('Начать', 'Отказаться')

back_menu = telebot.types.ReplyKeyboardMarkup(True)
back_menu.row('Назад')

del_markup = telebot.types.ReplyKeyboardRemove()

default = telebot.types.ReplyKeyboardMarkup(True)
default.row('Да', 'Нет')

sex = telebot.types.ReplyKeyboardMarkup(True)
sex.row('Мужской', 'Женский')

device = telebot.types.ReplyKeyboardMarkup(True)
device.row('Телефон', 'Компьютер')