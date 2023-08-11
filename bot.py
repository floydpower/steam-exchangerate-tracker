import asyncio
import json
import os
import requests

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

load_dotenv('config/.env')

bot = Bot(token=os.environ.get('BOT_TOKEN'), parse_mode='HTML')
dp = Dispatcher(bot)

CHANNEL_ID = os.environ.get('CHANNEL_ID')


def check_exchange_rate():
    response_usd = requests.get(
        'http://steamcommunity.com/market/priceoverview/?appid=440&currency=3&market_hash_name=Mann%20Co.%20Supply%20Crate%20Key')
    response_uah = requests.get(
        'http://steamcommunity.com/market/priceoverview/?appid=440&currency=18&market_hash_name=Mann%20Co.%20Supply%20Crate%20Key')
    price_usd = float(response_usd.json()['median_price'].replace(',', '.')[:-1])
    price_uah = float(response_uah.json()['median_price'].replace(',', '.')[:-1])
    return {
        'exchange_rate': (price_uah / price_usd).__round__(2)
    }


async def send_alert():
    while True:
        try:
            with open('cache/exchangerate_cache.json', 'r', encoding='utf-8') as json_file:
                data = json.load(json_file)

            new_prices = check_exchange_rate()

            if data['exchange_rate'] != new_prices['exchange_rate']:
                await bot.send_message(CHANNEL_ID,
                                       f'🔔 На торговому майданчику STEAM змінився курс долара до гривні: $1 = {new_prices["exchange_rate"]}₴')

            with open('cache/exchangerate_cache.json', 'w', encoding='utf-8') as json_file:
                json.dump(new_prices, json_file)

        except Exception as ex:
            print(f'Произошла ошибка - {ex}')

        finally:
            await asyncio.sleep(3600)
