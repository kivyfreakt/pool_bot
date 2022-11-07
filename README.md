# pool_bot

Телеграм бот для проведения опроса и составления портрета аудитории.

---

## Зависимости

Для приложения необходима библиотека **telebot** и другие

Полный список зависимостей находится в файле [requirements.txt](requirements.txt).

Установка всех зависимостей: 

``` bash
pip install -r requirements
```

## Настройка

Конфигурационный файл - [сonfig.py](config.py)

В файле необходимо задать aсcess token, полученный от bot father и идентификатор администратора

Файл [сonfig.py](config.py) должен выглядить так:

```

TOKEN_API = 'your token'
ADMIN = 00000000

```

Свои вопросы нужно указать в файле [questions.py](survey/questions.py)

Так же можно изменить стандартные ответы бота в фале [texts.py](survey/texts.py)

## Запуск

Запустить скрипт:

``` bash
python main.py
```

## Развертывание приложения

Сборка образа: 

``` bash
docker build -t pool_bot .
```

Запуск контейнера: 

``` bash
docker run -d --name bot pool_bot
```