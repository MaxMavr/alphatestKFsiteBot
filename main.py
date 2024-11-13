from config import *

from handlers.default import rt as default
from handlers.admin import rt as admin
from handlers.fill_preset import rt as fill_preset
from handlers.catch_bug import rt as catch_bug


async def main():
    dp: Dispatcher = Dispatcher()
    dp.include_router(default)
    dp.include_router(admin)
    dp.include_router(fill_preset)
    dp.include_router(catch_bug)
    await dp.start_polling(bot)

if __name__ == '__main__':
    print("Погнали ловить баги!")
    asyncio.run(main())
