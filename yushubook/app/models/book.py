# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, String

from app.models.base import Base


class Book(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(50), nullable=False)
    author = Column(String(50), nullable=True, default='未名')
    isbn = Column(String(50), nullable=False, unique=True)
    price = Column(String(50))
    binging = Column(String(50))
    publisher = Column(String(50))
    pubdate = Column(Integer)
    pages = Column(Integer)
    summary = Column(String(1000))
    image = Column(String(50))

    def sample(self):
        pass
