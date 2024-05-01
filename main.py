from aiogram import executor
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from settings import Settings
import handlers
import os
from database_operation import creating_data_base


def register_handlers(dp) -> None:
    handlers.register_callback_query_high(dp)
    handlers.register_callback_query_low(dp)
    handlers.register_main_handlers(dp)
    handlers.register_callback_query_handler_custom(dp)
    handlers.register_message_handler_custom(dp)


def main():
    tg = Settings()
    storage = MemoryStorage()
    bot = Bot(
        token=tg.bot_token.get_secret_value()
    )  # Здесь необходимо вставить токен бота
    dp = Dispatcher(bot=bot, storage=storage)

    executor.start_polling(
        dispatcher=dp, skip_updates=True, on_startup=register_handlers(dp)
    )


if __name__ == "__main__":
    if not os.path.exists("storage_photo"):
        os.mkdir("storage_photo")
    creating_data_base()
    main()
