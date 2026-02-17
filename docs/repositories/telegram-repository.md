## Telegram Token
You need to [obtain](https://docs.expertflow.com/cx/4.3/telegram-bot-creation-guide) a telegram token to use ***Telegram Repository***

After that you can easly put it in the `.env` under `TELEGRAM_BOT_TOKEN` variable:
```
TELEGRAM_BOT_TOKEN=your_token
```

## User

***User*** is the real user that would recive a message from your bot

### Where do I get the IDs?

There are many way to do so. Mostly you need a bot, like [userinfobot](https://t.me/UserinfoBot).

>***Be carefull do not trust anybody that wants your data, like phone / credit card number, etc***

>***We are not responsible for any of your losts (money, personal data, etc.)***

### What do I do with IDs?

You can add them into your `.env` file under `TELEGRAM_USER_IDS` variable:
```
TELEGRAM_USER_IDS=user_id1,user_id2
```

If you want multiple ***User***s, you can separate them with comma `,`
