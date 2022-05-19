#Alex Sparrow 17.05.2022
import logging, settings, ephem
from datetime import datetime
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='bot.log')

date_now = datetime.now().strftime('%Y-%m-%d')

planet_dict = {
    'Mars': ephem.Mars(date_now), 'Venus': ephem.Venus(date_now), 'Saturn': ephem.Saturn(date_now), 
    'Jupiter': ephem.Jupiter(date_now), 'Neptune': ephem.Neptune(date_now), 
    'Uranus': ephem.Uranus(date_now), 'Mercury': ephem.Mercury(date_now), 'Sun': ephem.Sun(date_now),
    }

def greet_user(update, context):
    text = 'Вызван /start'
    print(text)
    update.message.reply_text('Привет, пользователь! Ты вызвал команду /start')

def constellation_planet(update, context):
    text = 'Вызван /planet'
    print(text)
    user_text_list = update.message.text.split()
    planet = user_text_list[1].title()
    ephem_body = planet_dict.get(planet, None)
    if ephem_body != None:
        update.message.reply_text(f"{planet} сегодня находится в созвездии {ephem.constellation(planet_dict[planet])}")
    else:
        update.message.reply_text('Введена неизвестная планета')
    
def talk_to_me(update, context):
    user_text = update.message.text
    print(user_text)
    update.message.reply_text(user_text)

def main():
    mybot = Updater(settings.API_KEY, use_context=True)

    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("start", greet_user))
    dp.add_handler(CommandHandler("planet", constellation_planet))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))
    
    logging.info("Бот стартовал")
    mybot.start_polling()
    mybot.idle()

if __name__ == "__main__":
    main()