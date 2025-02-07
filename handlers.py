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
from messages import msg

from g4f_ai import generate_resp

router = Router()
lang = 'ru'

class Form(StatesGroup):
    processing = State()

class OrderStates(StatesGroup):
    order_description = State()

@router.message(CommandStart())
async def start(message: Message):
    await message.answer(msg[lang]['start_msg'], reply_markup=main_kb)

@router.message(F.text == msg[lang]['order_reading'])
async def crate_order(message: Message):
    await message.answer(msg[lang]['choose_master'])
    masters = await get_masters()
    for master in masters:
        await message.answer(f'{master['name']}\n{master['description']}', reply_markup=master_kb(master['id']))


@router.callback_query(F.data.startswith('master_'))
async def master_callback(callback: CallbackQuery):
    await callback.answer(msg[lang]['master_choosen'])
    prices = [LabeledPrice(label='XTR', amount=order_price)]
    await callback.message.answer_invoice(
        title=msg[lang]['order_reading'],
        description=msg[lang]['order_reading'],
        prices=prices,
        provider_token='',
        payload='order_reading',
        currency=CURRENCY,
        reply_markup=payment_kb(order_price)
    )

@router.pre_checkout_query(F.data == 'order_reading')
async def pre_checkout_query(pre_checkout_query: PreCheckoutQuery):
    await pre_checkout_query.answer(ok=True)

@router.message(F.successful_payment)
async def successful_payment(message: Message, state: FSMContext):
    await message.answer(msg[lang]['payment_was_successful'])
    order_payload = message.successful_payment.invoice_payload
    await message.answer(f'{msg[lang]["payload_of_order"]}\n{order_payload}')
    await message.answer(msg[lang]['query_for_master'])
    await state.update_data(order_payload=order_payload)
    await state.set_state(OrderStates.order_description)

@router.message(OrderStates.order_description)
async def order_description(message: Message, state: FSMContext):
    data = await state.get_data()
    payload = data.get('order_payload')
    await state.clear()
    await state.set_state(Form.processing)
    text = message.text
    await create_order(tg_id=message.from_user.id, text=text, order_datetime=datetime.now(), is_refunded=False, payload=payload, amount=order_price)
    await message.answer(msg[lang]['order_created'])
    response =  generate_resp(text)
    await asyncio.sleep(randint(500, 600))
    await message.answer(response)
    await state.clear()

@router.message(Form.processing)
async def processing(message: Message, state: FSMContext):
    await message.answer(msg[lang]['processing'])
