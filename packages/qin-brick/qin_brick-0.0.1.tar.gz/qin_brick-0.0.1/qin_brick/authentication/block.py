from qin_brick import Base
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import FetchedValue
from sqlalchemy import Integer
from sqlalchemy import String


class Block(Base):
    __tablename__ = 'block'

    id = Column(Integer, primary_key=True)
    uuid = Column(String(64), nullable=False, unique=True)
    name = Column(String(32, u'utf8_bin'), nullable=False)
    chinese_name = Column(String(32, u'utf8_bin'), nullable=False)
    status = Column(Integer, nullable=False)
    remark = Column(String(200, u'utf8_bin'), nullable=False)
    update_at = Column(DateTime, nullable=False)
    create_at = Column(DateTime, nullable=False, server_default=FetchedValue())
