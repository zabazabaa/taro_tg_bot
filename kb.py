from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from config import order_price

main_kb = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Заказать расклад')],
],
    resize_keyboard=True,
)

def master_kb(master_id: int):
    builder = InlineKeyboardBuilder()
    builder.button(text='Заказать', callback_data=f'master_{master_id}')
    return builder.as_markup()

def payment_kb(order_price: int):
    builder = InlineKeyboardBuilder()
    builder.button(text=f'Оплатить {order_price}⭐️', pay=True)
    return builder.as_markup()