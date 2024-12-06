from aiogram import Dispatcher, types
from config import SUPPORTED_FORMATS, RATES
from message import *
from kb import *
from aiogram.types import ReplyKeyboardMarkup


# Хранилище для данных
user_data = {}


# Функция для расчета стоимости печати
def calculate_price(pages, is_color, is_a3):
    price_per_page = RATES["color"] if is_color else RATES["black_white"]
    total = price_per_page * pages
    if is_a3:
        total *= RATES["a3_multiplier"]
    return round(total, 2)


# Хэндлер для стартового экрана
async def start_handler(message: types.Message):
    await message.answer(
        msg_welcome,
        reply_markup=ReplyKeyboardMarkup(resize_keyboard=True).add(
            btn_upload_file, btn_choose_location, btn_view_rates, btn_cart, btn_info, btn_help
        )
    )


# Обработка загрузки файла
async def upload_file_handler(message: types.Message):
    await message.answer(msg_upload_file)


async def file_received_handler(message: types.Message):
    # Проверка файла
    if not message.document:
        await message.answer(msg_file_error)
        return

    file_extension = message.document.file_name.split('.')[-1].lower()
    if file_extension not in SUPPORTED_FORMATS:
        await message.answer(msg_file_error)
        return

    # Сохранение файла
    user_id = message.from_user.id
    user_data[user_id] = {"cart": [], "current_file": {
        "file_id": message.document.file_id,
        "file_name": message.document.file_name,
        "pages": 1,
        "is_color": False,
        "is_a3": False,
    }}
    await message.answer(
        msg_print_settings,
        reply_markup=ReplyKeyboardMarkup(resize_keyboard=True).add(
            btn_add_to_cart, btn_change_parameters, btn_cancel
        )
    )


# Обработка изменения параметров печати
async def change_parameters_handler(message: types.Message):
    user_id = message.from_user.id
    current_file = user_data.get(user_id, {}).get("current_file")
    if not current_file:
        await message.answer(msg_error_generic)
        return

    # Пример изменения параметров
    current_file["pages"] = 10
    current_file["is_color"] = True
    current_file["is_a3"] = False

    price = calculate_price(
        current_file["pages"], current_file["is_color"], current_file["is_a3"]
    )
    await message.answer(
        f"Параметры обновлены:\n"
        f"Страниц: {current_file['pages']}, Цветная: {'Да' if current_file['is_color'] else 'Нет'}, "
        f"A3: {'Да' if current_file['is_a3'] else 'Нет'}\nСтоимость: {price} руб.",
        reply_markup=ReplyKeyboardMarkup(resize_keyboard=True).add(
            btn_add_to_cart, btn_cancel
        )
    )


# Обработка добавления в корзину
async def add_to_cart_handler(message: types.Message):
    user_id = message.from_user.id
    current_file = user_data.get(user_id, {}).pop("current_file", None)
    if not current_file:
        await message.answer(msg_error_generic)
        return

    price = calculate_price(
        current_file["pages"], current_file["is_color"], current_file["is_a3"]
    )
    current_file["price"] = price
    user_data[user_id]["cart"].append(current_file)
    await message.answer(
        msg_file_added_to_cart,
        reply_markup=ReplyKeyboardMarkup(resize_keyboard=True).add(
            btn_upload_file, btn_cart, btn_choose_location
        )
    )


# Обработка корзины
async def cart_handler(message: types.Message):
    user_id = message.from_user.id
    cart = user_data.get(user_id, {}).get("cart", [])
    if not cart:
        await message.answer(msg_cart_empty)
        return

    cart_details = "\n".join([f"{item['file_name']} — {item['price']} руб." for item in cart])
    total_price = sum(item['price'] for item in cart)
    await message.answer(
        msg_cart_details.format(cart_details=cart_details, total_price=total_price),
        reply_markup=ReplyKeyboardMarkup(resize_keyboard=True).add(
            btn_checkout, btn_edit_parameters, btn_delete_file, btn_change_print_location, btn_back
        )
    )


# Обработка просмотра тарифов
async def view_rates_handler(message: types.Message):
    await message.answer(
        msg_view_rates,
        reply_markup=ReplyKeyboardMarkup(resize_keyboard=True).add(btn_back)
    )


# Обработка информации о сервисе
async def info_handler(message: types.Message):
    await message.answer(
        msg_info,
        reply_markup=ReplyKeyboardMarkup(resize_keyboard=True).add(btn_back)
    )


# Обработка помощи
async def help_handler(message: types.Message):
    await message.answer(
        msg_help,
        reply_markup=ReplyKeyboardMarkup(resize_keyboard=True).add(btn_back)
    )


# Обработка возврата назад
async def back_handler(message: types.Message):
    await start_handler(message)

# Выбор локации 
async def choose_location_handler(message: types.Message):
    await message.answer(
        msg_location_list,
        reply_markup=ReplyKeyboardMarkup(resize_keyboard=True).add(btn_back)
    )

# Подключение хэндлеров
def register_handlers(dp: Dispatcher):
    dp.register_message_handler(start_handler, commands=["start"])
    dp.register_message_handler(upload_file_handler, text=btn_upload_file)
    dp.register_message_handler(file_received_handler, content_types=["document"])
    dp.register_message_handler(change_parameters_handler, text=btn_change_parameters)
    dp.register_message_handler(add_to_cart_handler, text=btn_add_to_cart)
    dp.register_message_handler(cart_handler, text=btn_cart)
    dp.register_message_handler(view_rates_handler, text=btn_view_rates)
    dp.register_message_handler(info_handler, text=btn_info)
    dp.register_message_handler(help_handler, text=btn_help)
    dp.register_message_handler(back_handler, text=btn_back)
    dp.register_message_handler(choose_location_handler, text=btn_choose_location)

