#Alex Sparrow 17.05.2022

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging, settings
from handlers import (greet_user, get_word_count, send_cat_picture,
talk_to_me, constellation_planet, next_full_moon, guess_number, user_coordinates)

logging.basicConfig(filename='bot.log', level=logging.INFO)


def main():
    mybot = Updater(settings.API_KEY, use_context=True)

    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("start", greet_user))
    # dp.add_handler(CommandHandler("cities", game_cities))
    dp.add_handler(CommandHandler("planet", constellation_planet))
    dp.add_handler(CommandHandler("nextfullmoon", next_full_moon))
    dp.add_handler(CommandHandler("wordcount", get_word_count))
    dp.add_handler(CommandHandler("guess", guess_number))
    dp.add_handler(CommandHandler("cat", send_cat_picture))
    dp.add_handler(MessageHandler(Filters.regex('^(Прислать котика)$'), send_cat_picture))
    dp.add_handler(MessageHandler(Filters.location, user_coordinates))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))

    logging.info("Bot is start")
    mybot.start_polling()
    mybot.idle()


if __name__ == "__main__":
    main()