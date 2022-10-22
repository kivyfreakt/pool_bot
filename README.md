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

В файле необходимо задать aсcess token, полученный от bot father

Файл [сonfig.py](config.py) должен выглядить так:

```

token_api = 'your token'

```

Свои вопросы нужно указать в файле [questions.py](survey/questions.py)

Так же можно изменить стандартные ответы бота в фале [texts.py](survey/texts.py)

## Запуск

Запустить скрипт:

``` bash
python main.py
```

<!-- ## Развертывание приложения

Сборка образа: 

``` bash
	docker build .
```

Запуск контейнера: 

``` bash
	docker run
``` -->