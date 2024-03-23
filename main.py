import telebot
import os
import requests
import json
import time
import math
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

bot = telebot.TeleBot(os.getenv('TOKEN_TELEBOT'), parse_mode=None)

# --- User control ---- #
MIN_SUM_ASK = 1000000
MIN_SUM_BID_FIRST = 1000000
MIN_SUM_BIDS_SECOND = 300000
LIMIT = 5
LEVEL = 5
TIMEOUT = 5  # Enter timeouts in seconds
API_URL = f'{os.getenv('ROOT_API_URL')}/v4/public/orderbook/WBT_USDT?limit={LIMIT}&level={LEVEL}'


# --- User control ---- #

def handle_asks(asks):
    return math.trunc(float(asks[0][0]) * float(asks[0][1]))


def handle_bids_first(bids):
    return math.trunc(float(bids[0][0]) * float(bids[0][1]))


def handle_bids_second(bids):
    return math.trunc(float(bids[1][0]) * float(bids[1][1]))


def check_value_asks(value):
    if value < MIN_SUM_ASK:
        return True
    else:
        return False


def check_value_bids_first(value):
    if value > MIN_SUM_BID_FIRST:
        return True
    else:
        return False


def check_value_bids_second(value):
    if value < MIN_SUM_BIDS_SECOND:
        return True
    else:
        return False


@bot.message_handler(commands=['start', ])
def welcome(message):
    bot.reply_to(message, f'Hello, {message.from_user.first_name}')
    while True:
        try:
            response = requests.get(API_URL)
            asks = json.loads(response.text)['asks']
            bids = json.loads(response.text)['bids']

            if check_value_asks(handle_asks(asks)):
                bot.send_message(chat_id=message.chat.id, text="Go trading! It is < than 1 000 000!")

            if check_value_bids_first(handle_bids_first(bids)):
                bot.send_message(chat_id=message.chat.id, text="Go trading! It is > than 1 000 000!")

            if check_value_bids_second(handle_bids_second(bids)):
                bot.send_message(chat_id=message.chat.id, text="Go trading! It is < than 300 000!")

        except Exception as e:
            print(f'Something wint wrong with {e}')

        time.sleep(TIMEOUT)


print('Polling...')
bot.infinity_polling()
