# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, String, SmallInteger

from app.lib.enums import PendingStatus
from app.models.base import Base


class Drift(Base):
    id = Column(Integer, primary_key=True)

    # 邮寄信息
    recipient_name = Column(String(20), nullable=False, comment='收件人姓名')
    address = Column(String(100), nullable=False, comment='收件地址')
    message = Column(String(200))
    mobile = Column(String(20), nullable=False)

    # 书籍信息
    isbn = Column(String(13))
    book_title = Column(String(50))
    book_author = Column(String(30))
    book_img = Column(String(50))

    # 请求者信息
    requester_id = Column(Integer)
    requester_nickname = Column(String(20))
    # 十一月

    # 赠送者信息
    gifter_id = Column(Integer)
    gift_id = Column(Integer)
    gifter_nickname = Column(String(20))

    _pending = Column('pending', SmallInteger, default=1, comment='交易状态')

    @property
    def pending(self):
        return PendingStatus(self._pending)  # 数字类型转枚举类型

    @pending.setter
    def pending(self, status):
        self._pending = status.value  # 枚举转数字
