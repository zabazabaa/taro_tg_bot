from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from config import order_price
from messages import msg
lang = 'ru'

main_kb = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text=msg[lang]['order_reading'])],
],
    resize_keyboard=True,
)

def master_kb(master_id: int):
    builder = InlineKeyboardBuilder()
    builder.button(text=msg[lang]['order'], callback_data=f'master_{master_id}')
    return builder.as_markup()

def payment_kb(order_price: int):
    builder = InlineKeyboardBuilder()
    builder.button(text=f'{msg[lang]["pay"]} {order_price}⭐️', pay=True)
    return builder.as_markup()