from typing import List

from qin_brick import Base
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import FetchedValue
from sqlalchemy import Integer
from sqlalchemy import String


class Product(Base):
    __tablename__ = 'product'
    __bind_key__ = 'guard'

    id = Column(Integer, primary_key=True)
    service_name = Column(String(100), nullable=False, unique=True)
    mode = Column(String(128), nullable=False)
    name = Column(String(100, u'utf8_bin'), nullable=False)
    description = Column(String(255, u'utf8_bin'), nullable=False)
    path = Column(String(100, u'utf8_bin'))
    user_id = Column(String(100), nullable=False, index=True)
    status = Column(Integer, nullable=False, server_default=FetchedValue())
    update_at = Column(DateTime)
    create_at = Column(DateTime, nullable=False, server_default=FetchedValue())
    delete_at = Column(DateTime)

    @classmethod
    def get_all(cls) -> List['Product']:
        return cls.query.all()
