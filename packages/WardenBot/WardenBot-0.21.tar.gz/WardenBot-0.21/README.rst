WardenBot
=========

.. image:: http://dadard.fr:8080/api/badges/dadard/WardenBot/status.svg
	:target: http://dadard.fr:8080/api/badges/dadard/WardenBot/status.svg

.. image:: https://badge.fury.io/py/WardenBot.svg
    :target: https://badge.fury.io/py/WardenBot

This is a goddamn bot

WHY
---

In Grafana, you have the option to bind an alert from your metrics data, to a Telegram Bot (see doc_).

.. _doc: https://core.telegram.org/bots

This is convenient to be alerted via instant messaging (no delay, few of configuration needed...)

HOW
---

Bot examples are given here_.

.. _here: https://github.com/python-telegram-bot/python-telegram-bot/tree/master/examples

By reading the official docs, you should have get a **Bot Token**. Store it in a secure way and retrieve it in your code (I personally store the bot token in an environment variable in a container)

Dont forget to install the ``python-telegram-bot`` package when copy/pasting examples :)

When the code of your bot is ready, deploy it or launch it : ``python your_bot.py``. If dockerized, use ``docker run -d warden_bot``.

In Telegram Messaging App, you should be able to start a new group, and to add your bot in.

The last thing you need is the Chat ID of the group you just created. To retrieve it, checkout the Telegram Api :
``https://api.telegram.org/bot{BOT_TOKEN}/getUpdates``

In case of troubles, see this post_.

.. _post: https://stackoverflow.com/questions/32423837/telegram-bot-how-to-get-a-group-chat-id

Then, just put the chat ID and the bot ID in your Grafana alert handler and test it.
