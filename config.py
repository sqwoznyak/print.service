import os

# Токен вашего бота
BOT_TOKEN = os.getenv("BOT_TOKEN", "YOUR_BOT_TOKEN_PASTE_HERE")

# Поддерживаемые форматы файлов
SUPPORTED_FORMATS = ['pdf', 'docx', 'png', 'jpg']

# Тарифы
RATES = {
    "black_white": 5,  # руб. за страницу
    "color": 10,  # руб. за страницу
}
