import asyncio
import logging
from aiogram import Bot, Dispatcher
from routers.command_routers import command_rout
from routers.send_routers import send_rout
from jsons.work_with_json import TOKEN


async def main() -> None:
    dp = Dispatcher()
    dp.include_routers(command_rout)
    dp.include_routers(send_rout)
    bot = Bot(TOKEN)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        logging.basicConfig(level=logging.INFO)
        asyncio.run(main())
    except KeyboardInterrupt:
        print("End...")
