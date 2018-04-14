from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import *
from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.types import Integer, String

Base = declarative_base()

class OrderBook(Base):
    __tablename__ = 'orderbook'
    id = Column(Integer,primary_key=True)
    typ = Column(String, nullable=False)
    price = Column(String,nullable=False)
    count = Column(String,nullable=False)
    amount = Column(String,nullable=False)
    xchange = Column(String, nullable=False)

class Main():
    def __init__(self):
        pass

    def __del__(self):
        pass

    def run(session, msglist):
        #insert
        o1 = OrderBook()
        o1.typ= msglist[0]
        o1.amount = msglist[3]
        o1.price = msglist[1]
        o1.count = msglist[2]
        o1.xchange = msglist[4]

        session.add(o1)
        session.commit()

