from aiogram import Bot, Dispatcher, executor
from config import BOT_TOKEN
from handlers import register_handlers

# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

# Регистрация хэндлеров
register_handlers(dp)

if __name__ == "__main__":
    print("Бот запущен!")
    executor.start_polling(dp, skip_updates=True)

