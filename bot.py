#Alex Sparrow 17.05.2022
import logging, settings, ephem
from datetime import date
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='bot.log')


def greet_user(update, context):
    text = 'Вызван /start'
    print(text)
    update.message.reply_text('Привет, пользователь! Ты вызвал команду /start')


def constellation_planet(update, context):
    text = 'Вызван /planet'
    print(text)
    user_text_list = update.message.text.split()
    planet = user_text_list[1].title()
    ephem_body = getattr(ephem, planet, 'Error')
    if ephem_body != 'Error':
        update.message.reply_text(f"{planet} сегодня находится в созвездии "\
        f"{ephem.constellation(ephem_body(date.today()))}")
    else:
        update.message.reply_text("Введена неизвестная планета")

# isinstance(user_text, str)
def get_word_count(update, context):
    text = 'Вызван /wordcount'
    print(text)
    word_list = update.message.text.split()
    wordcount = 0
    for word in word_list[1:]:
        if isinstance(word, str) and word != '-':
            wordcount += 1
            try:
                if isinstance(int(word), int):
                    wordcount -= 1
            except ValueError:
                print("ValueError")
    if wordcount >= 1:
        update.message.reply_text(f"Количество слов "\
        f"в предложении - {wordcount}")
    else:
        update.message.reply_text("Введите /wordcount 'текст'")


def talk_to_me(update, context):
    user_text = update.message.text
    print(user_text)
    update.message.reply_text(user_text)


def main():
    mybot = Updater(settings.API_KEY, use_context=True)

    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("start", greet_user))
    dp.add_handler(CommandHandler("planet", constellation_planet))
    dp.add_handler(CommandHandler("wordcount", get_word_count))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))

    logging.info("Бот стартовал")
    mybot.start_polling()
    mybot.idle()


if __name__ == "__main__":
    main()