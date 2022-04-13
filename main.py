import logging

from aiogram import executor
from aiogram.contrib.middlewares.logging import LoggingMiddleware



import config
import weather.weather_main
from handlers.users import my_requests
from handlers.users import sup
from loader import dp, bot, storage

my_requests.reg_requests(dp)
sup.reg_hadlers_sup(dp)
weather.weather_main.reg_weather(dp)

dp.middleware.setup(LoggingMiddleware())
logging.basicConfig(level=logging.INFO)

# webhook settings
WEBHOOK_HOST = 'https://mnimidemo.baldcatdev.com'
WEBHOOK_PATH = '/'
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

# webserver settings
WEBAPP_HOST = 'localhost'  # or ip
WEBAPP_PORT = 8443


async def on_shutdown_pool(dp):
    await storage.close()
    await bot.close()


async def on_startup(dp):
    await bot.set_webhook(WEBHOOK_URL)
    print(await bot.get_webhook_info())


async def on_shutdown(dp):
    logging.warning('Shutting down..')
    await storage.close()
    await bot.delete_webhook()
    logging.warning('Bye!')


# # Run bot
# print(f"Running bot in webhook mode.")
# executor.start_webhook(
#     dispatcher=dp,
#     webhook_path=WEBHOOK_PATH,
#     on_startup=on_startup,
#     on_shutdown=on_shutdown,
#     skip_updates=True,
#     host=WEBAPP_HOST,
#     port=WEBAPP_PORT,
# )
# Run bot
if config.APP_NAME is None:  # pooling mode
    print("Can't detect 'HEROKU_APP_NAME' env. Running bot in pooling mode.")
    print("Note: this is not a great way to deploy the bot in Heroku.")

    executor.start_polling(dp, on_shutdown=on_shutdown_pool, skip_updates=True)

# webhook mode
else:
    print(f"Running bot in webhook mode.")
    executor.start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        skip_updates=True,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT,
    )
