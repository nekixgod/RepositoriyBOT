import asyncio
import logging
import sys
import os

# Добавляем путь к папке book_bot в sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)  # Поднимаемся на уровень выше book_bot
sys.path.insert(0, project_root)

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage

try:
    from config.config import Config, load_config
    from handlers.user import router as user_handlers
    from handlers.other import router as other_handlers
    from keyboards.menu_commands import set_main_menu
    from database.database import init_db

    print("✅ Все импорты успешны!")
except ImportError as e:
    print(f"❌ Ошибка импорта: {e}")
    print("Текущая директория:", os.getcwd())
    print("Python path:", sys.path)
    sys.exit(1)

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(filename)s:%(lineno)d #%(levelname)-8s '
           '[%(asctime)s] - %(name)s - %(message)s'
)

logger = logging.getLogger(__name__)

async def main():
    logger.info('Starting bot')

    # Загружаем конфиг
    config: Config = load_config()

    if not config.tg_bot.token:
        logger.error("❌ BOT_TOKEN не найден в .env файле")
        return

    storage = MemoryStorage()

    # Создаем бота с правильными параметрами для aiogram 3.23.0
    bot = Bot(
        token=config.tg_bot.token,
        default=DefaultBotProperties(parse_mode='HTML')
    )
    dp = Dispatcher(storage=storage)

    # Инициализируем БД и меню
    await init_db()
    await set_main_menu(bot)

    # Подключаем роутеры
    dp.include_router(user_handlers)
    dp.include_router(other_handlers)

    # Удаляем вебхук и запускаем поллинг
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())