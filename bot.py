#Alex Sparrow 17.05.2022

from datetime import date
from emoji import emojize
from glob import glob
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from random import choice, randint
from telegram import ReplyKeyboardMarkup
import ephem, logging, settings

logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='bot.log')

cities_list = ['Москва', 'Архангельск', 'Калуга', 'Армавир', 
'Рязань', 'Нижний-Новгород'] #как работать с большими списками?


def get_smile(user_data):
    if 'emoji' not in user_data:
        smile = choice(settings.USER_EMOJI)
        return emojize(smile, use_aliases=True)
    return user_data['emoji']


def greet_user(update, context):
    text = 'Вызван /start'
    print(text)
    context.user_data['emoji'] = get_smile(context.user_data)
    my_keyboard = ReplyKeyboardMarkup([['Прислать котика']])
    update.message.reply_text(
        f"Здравствуй, пользователь {context.user_data['emoji']}!",
        reply_markup=my_keyboard
    )


def talk_to_me(update, context):
    context.user_data['emoji'] = get_smile(context.user_data)
    username = update.effective_user.first_name
    text = update.message.text
    update.message.reply_text(
        f"Здравствуй, {username} {context.user_data['emoji']}! Ты написал: {text}"
    )


"""def game_cities(update, context):
    text = 'Вызван /cities'
    print(text)
    if context.args:
        user_city = context.args[0]
        cities_copy = cities_list[:]
        while len(cities_copy) > 0:
            for index in range(len(cities_copy)):
                if user_city[-1].upper() == cities_copy[index][0]:
                    message = f"{cities_copy[index]}, ваш ход"
                    update.message.reply_text(message)
                    cities_copy.remove(cities_copy[index])
                    user_city = talk_to_me(update, context)
                    break
    else:
        message = "Введите название города"
        update.message.reply_text(message)"""


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
        if isinstance(word, str) and word != '-': #можно проверять также на входимость word в список из спецсимолов
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


def play_random_numbers(user_number):
    bot_number = randint(user_number-10, user_number+10)
    if user_number > bot_number:
        message = f"Ты загадал {user_number}, я загадал {bot_number}, ты выиграл!"
    elif user_number == bot_number:
        message = f"Ты загадал {user_number}, я загадал {bot_number}, ничья!"
    else:
        message = f"Ты загадал {user_number}, я загадал {bot_number}, я выиграл!"
    return message


def guess_number(update, context):
    text = 'Вызван /guess'
    print(text)
    if context.args:
        try:
            user_number = int(context.args[0])
            message = play_random_numbers(user_number)
        except (TypeError, ValueError):
            message = "Введите целое число"
    else:
        message = "Введите целое число"
    update.message.reply_text(message)


def send_cat_picture(update, context):
    cat_photos_list = glob('images/cat*.jp*g')
    cat_pic_filename = choice(cat_photos_list)
    chat_id = update.effective_chat.id
    context.bot.send_photo(chat_id=chat_id, photo=open(cat_pic_filename, 'rb'))


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
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))

    logging.info("Bot is start")
    mybot.start_polling()
    mybot.idle()


if __name__ == "__main__":
    main()