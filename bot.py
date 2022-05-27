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


def game_cities(update, context):
    text = 'Вызван /cities'
    print(text)
    cities_list = ['Москва', 'Архангельск', 'Калуга', 'Армавир',
    'Рязань', 'Нижний-Новгород'] #как работать с большими списками?
    cities_copy = cities_list[:]
    user_text_list = update.message.text.split()
    city = user_text_list[1].title()
    for index in range(len(cities_copy)):
        if city in cities_copy:
            cities_copy.remove(city)
        if city[-1].upper() == cities_copy[index][0]:
            update.message.reply_text(f"{cities_copy[index]}, ваш ход")
            cities_copy.remove(cities_copy[index])
            # city = update.message.text.upper()
            break
        else:
            update.message.reply_text("Я сдаюсь")


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


def next_full_moon(update, context):
    text = 'Вызван /nextfullmoon'
    print(text)
    update.message.reply_text(f"Ближайшее полнолуние - "\
        f"{ephem.next_full_moon(date.today())}")


def talk_to_me(update, context):
    user_text = update.message.text
    print(user_text)
    update.message.reply_text(user_text)


def main():
    mybot = Updater(settings.API_KEY, use_context=True)
    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("start", greet_user))
    dp.add_handler(CommandHandler("cities", game_cities))
    dp.add_handler(CommandHandler("planet", constellation_planet))
    dp.add_handler(CommandHandler("nextfullmoon", next_full_moon))
    dp.add_handler(CommandHandler("wordcount", get_word_count))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))
    logging.info("Bot is start")
    mybot.start_polling()
    mybot.idle()


if __name__ == "__main__":
    main()