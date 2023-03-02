# pool_bot

Telegram bot for conducting a survey and compiling a portrait of the audience.

---

## Dependencies

The application requires the **telebot** library and others

A complete list of dependencies can be found in the [requirements.txt](requirements.txt) file.

Installing all dependencies: 

``` bash
pip install -r requirements
```

## Setting up

The configuration file is [config.py](config.py)

In the file you must specify the access token received from the bot father and the ID of the administrator

The [config.py](config.py) file should look like this:

```

TOKEN_API = 'your token'
ADMIN = 00000000

```

You need to specify your questions in the file [questions.py](survey/questions.py)

You can also change the bot's default responses in the [texts.py] file (survey/texts.py)

## Starting the application

Run the script:

``` bash
python main.py
```

## Deploying the application

Build a docker image: 

``` bash
docker build -t pool_bot .
```

Running the docker container:

``` bash
docker run -d --name bot pool_bot
```
