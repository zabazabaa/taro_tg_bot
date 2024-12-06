import asyncio
from aiogram.types import Message, PreCheckoutQuery, LabeledPrice
from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from datetime import datetime
from random import randint

from db.crud import get_masters, create_order

from kb import main_kb, master_kb, payment_kb
from config import CURRENCY, order_price

from g4f_ai import generate_resp

router = Router()

class Form(StatesGroup):
    processing = State()

class OrderStates(StatesGroup):
    order_description = State()

@router.message(CommandStart())
async def start(message: Message):
    await message.answer('Добро пожаловать в бота!', reply_markup=main_kb)

@router.message(F.text == 'Заказать расклад')
async def crate_order(message: Message, state: FSMContext):
    await message.answer('Выберите мага')
    masters = await get_masters()
    for master in masters:
        await message.answer(f'{master['name']} - {master['description']}', reply_markup=master_kb(master['id']))


@router.callback_query(F.data.startswith('master_'))
async def master_callback(callback: CallbackQuery, state: FSMContext):
    master_id = callback.data.split('_')[1]
    await callback.answer('Выбран мастер')
    prices = [LabeledPrice(label='XTR', amount=order_price)]
    await callback.message.answer_invoice(
        title='Заказать расклад',
        description='Заказать расклад у мага',
        prices=prices,
        provider_token='',
        payload='buy_rasklad',
        currency=CURRENCY,
        reply_markup=payment_kb(order_price)
    )

@router.pre_checkout_query(F.data == 'buy_rasklad')
async def pre_checkout_query(pre_checkout_query: PreCheckoutQuery):
    await pre_checkout_query.answer(ok=True)

@router.message(F.successful_payment)
async def successful_payment(message: Message, state: FSMContext):
    await message.answer('Оплата проведена успешно')
    await message.answer('Введите запрос для мага:')
    await state.set_state(OrderStates.order_description)

@router.message(OrderStates.order_description)
async def order_description(message: Message, state: FSMContext):
    await state.clear()
    await state.set_state(Form.processing)
    text = message.text
    await create_order(tg_id=message.from_user.id, text=text, order_datetime=datetime.now(), is_refunded=False)
    await message.answer('Заказ успешно создан\тОжидайте около 10 минут')
    response =  generate_resp(text)
    await asyncio.sleep(randint(500,600))
    await message.answer(response)

@router.message(Form.processing)
async def processing(message: Message, state: FSMContext):
    await message.answer('Ожидайте ответа...')

@router.message(F.text == 'freeGPT')
async def freeGPT_cmd(message: Message):
    await message.answer('Заказ успешно создан')
    response =  generate_resp('Будит ли арина 23 и Иван 24 вместе')
    await message.answer(response)