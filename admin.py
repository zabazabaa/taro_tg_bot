from aiogram import Router, Bot
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message
from aiogram.filters import Command
from functools import wraps

from db.crud import add_admin, add_master, check_admin_by_tgid

admin_router = Router()

class MasterStates(StatesGroup):
    add_master_name = State()
    add_master_description = State()

def admin_only(handler):
    @wraps(handler)
    async def wrapper(message: Message, *args, **kwargs):
        # Проверка, является ли пользователь администратором
        if not await check_admin_by_tgid(message.from_user.id):
            await message.reply("У вас нет прав для выполнения этой команды.")
            return
        return await handler(message, *args, **kwargs)
    return wrapper

@admin_router.message(Command('admin'))
@admin_only
async def admin_cmd(message: Message):
    await message.answer("""Команды:
/refound ID_ЗАКАЗА
/add_master
""")

@admin_router.message(Command('add_master'))
@admin_only
async def add_master_cmd(message: Message, state: FSMContext):
    await message.answer('Введите имя мастера')
    await state.set_state(MasterStates.add_master_name)

@admin_router.message(MasterStates.add_master_name)
@admin_only
async def add_master_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer('Введите описание мастера')
    await state.set_state(MasterStates.add_master_description)

@admin_router.message(MasterStates.add_master_description)
@admin_only
async def add_master_description(message: Message, state: FSMContext):
    data = await state.get_data()
    await add_master(data['name'], message.text)
    await state.clear()
    await message.answer('Мастер успешно добавлен')

@admin_router.message(Command('refound'))
@admin_only
async def refound_cmd(message: Message, bot: Bot, command: Command):
    command_text = message.text.lstrip('/refound').strip()
    if command_text:
        ...
    else:
        await message.answer('Перадайте ID заказа\n/refound ID_ЗАКАЗА')