import asyncio
import logging
from datetime import datetime
import pytz
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.filters import Command
import os

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Получаем токен бота из переменных окружения bothost.ru
BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    logger.error("❌ Не задана переменная окружения BOT_TOKEN")
    exit(1)

# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: Message):
    """Обработчик команды /start"""
    await message.answer(
        "🕐 Бот времени сервера\n\n"
        "Доступные команды:\n"
        "/time - текущее время на сервере\n"
        "/date - текущая дата на сервере\n"
        "/datetime - полная дата и время"
    )

@dp.message(Command("time"))
async def cmd_time(message: Message):
    """Обработчик команды /time - возвращает текущее время"""
    try:
        # Получаем текущее время на сервере
        server_time = datetime.now().strftime("%H:%M:%S")
        timezone = datetime.now().astimezone().tzname()
        
        await message.answer(f"🕐 Текущее время на сервере: {server_time} ({timezone})")
        logger.info(f"Отправлено время: {server_time}")
    except Exception as e:
        logger.error(f"Ошибка при получении времени: {e}")
        await message.answer("❌ Ошибка при получении времени")

@dp.message(Command("date"))
async def cmd_date(message: Message):
    """Обработчик команды /date - возвращает текущую дату"""
    try:
        # Получаем текущую дату на сервере
        server_date = datetime.now().strftime("%d.%m.%Y")
        
        await message.answer(f"📅 Текущая дата на сервере: {server_date}")
        logger.info(f"Отправлена дата: {server_date}")
    except Exception as e:
        logger.error(f"Ошибка при получении даты: {e}")
        await message.answer("❌ Ошибка при получении даты")

@dp.message(Command("datetime"))
async def cmd_datetime(message: Message):
    """Обработчик команды /datetime - возвращает полную дату и время"""
    try:
        # Получаем полную дату и время на сервере
        server_datetime = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        timezone = datetime.now().astimezone().tzname()
        
        await message.answer(f"📅🕐 Дата и время на сервере: {server_datetime} ({timezone})")
        logger.info(f"Отправлена дата и время: {server_datetime}")
    except Exception as e:
        logger.error(f"Ошибка при получении даты и времени: {e}")
        await message.answer("❌ Ошибка при получении даты и времени")

async def send_daily_time_notification(chat_id: str):
    """Функция для отправки ежедневного уведомления о времени"""
    try:
        current_time = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        timezone = datetime.now().astimezone().tzname()
        
        await bot.send_message(
            chat_id=chat_id,
            text=f"📊 Ежедневное уведомление:\nВремя на сервере: {current_time} ({timezone})"
        )
        logger.info(f"Отправлено ежедневное уведомление в чат {chat_id}")
    except Exception as e:
        logger.error(f"Ошибка при отправке ежедневного уведомления: {e}")

async def main():
    """Основная функция запуска бота"""
    logger.info("🚀 Запуск бота времени...")
    
    try:
        # Запускаем бота
        await dp.start_polling(bot)
    except Exception as e:
        logger.error(f"❌ Ошибка при запуске бота: {e}")
    finally:
        # Закрываем сессию бота при завершении
        await bot.session.close()
        logger.info("✅ Бот завершил работу")

if __name__ == "__main__":
    asyncio.run(main())