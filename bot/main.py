from aiogram.utils import executor
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from bot import settings
from bot.handlers import register_private_chat_handlers, register_general_chat_handlers, register_temp_chat_handlers


def _on_startup(dp: Dispatcher):
    register_private_chat_handlers(dp)
    register_general_chat_handlers(dp)


def main():
    bot = Bot(token=settings.TOKEN, parse_mode='HTML')
    dispatcher = Dispatcher(bot=bot, storage=MemoryStorage())
    executor.start_polling(dispatcher=dispatcher, skip_updates=True, on_startup=_on_startup(dp=dispatcher))
