import asyncio
from aiogram import executor
from bot import dp, send_alert

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(send_alert())
    executor.start_polling(dp, skip_updates=True)
