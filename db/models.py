from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Time, Date, ForeignKey

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    tg_id = Column(Integer, nullable=False)
    ballance = Column(Integer, nullable=False)

class Master(Base):
    __tablename__ = 'masters'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)

class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True)
    tg_id = Column(Integer, nullable=False)
    order_datetime = Column(DateTime, nullable=False)
    text = Column(String, nullable=False)
    is_refunded = Column(Boolean, nullable=False)
    order_id = Column(String, nullable=False)
    amount = Column(Integer, nullable=False)
    
class Admin(Base):
    __tablename__ = 'admins'
    id = Column(Integer, primary_key=True)
    tg_id = Column(Integer, nullable=False)
#    username = Column(String, nullable=False)
#    password_hash = Column(String, nullable=False)