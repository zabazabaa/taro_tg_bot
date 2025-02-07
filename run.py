import asyncio
from aiogram import Bot, Dispatcher
from os import getenv
from dotenv import load_dotenv

from handlers import router
from admin import admin_router

from db.session import init_db

async def main():
    load_dotenv()
    await init_db()
    bot = Bot(getenv('BOT_TOKEN'))
    dp = Dispatcher()
    dp.include_router(router)
    dp.include_router(admin_router)
    await dp.start_polling(bot)

if __name__ == '__main__':
    #asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())  #use this on windows
    asyncio.run(main())