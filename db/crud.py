from sqlalchemy.future import select
from datetime import datetime

from db.session import async_session
from db.models import User, Master, Order, Admin

async def check_admin_by_tgid(tg_id: int):
    async with async_session() as session:
        async with session.begin(): 
            admin = await session.execute(select(Admin).where(Admin.tg_id == tg_id))
            return admin.scalar_one_or_none()

async def add_admin(tg_id: int):
    async with async_session() as session:
        async with session.begin():
            admin = Admin(tg_id=tg_id)
            session.add(admin)
            await session.commit()

async def add_master(name: str, description: str):
    async with async_session() as session:
        async with session.begin():
            master = Master(name=name, description=description)
            session.add(master)
            await session.commit()
            
async def get_masters():
    async with async_session() as session:
        async with session.begin():
            masters = await session.execute(select(Master))
            result = masters.scalars().all()
            return [{'id': master.id, 'name': master.name, 'description': master.description} for master in result]

async def create_order(tg_id: int, text: str, order_datetime: datetime, payload: str, amount: int):
    async with async_session() as session:
        async with session.begin():
            order = Order(tg_id=tg_id, text=text, order_datetime=order_datetime, is_refunded=False, payload=payload, amount=amount)
            session.add(order)
            await session.commit()