from typing import List, Dict, Any

from qin_brick import Base
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import FetchedValue
from sqlalchemy import Integer
from sqlalchemy import String


class Company(Base):
    __tablename__ = 'company'
    __bind_key__ = 'guard'

    id = Column(Integer, primary_key=True)
    uuid = Column(String(36), nullable=False, unique=True)
    name = Column(String(32, u'utf8_bin'), nullable=False)
    encryption_type = Column(Integer, nullable=False)
    company_pub_secret_key = Column(String(1024), nullable=False)
    producer_prv_secret_key = Column(String(2048), nullable=False)
    aes_key = Column(String(255), nullable=False)
    contact_person = Column(String(20, u'utf8_bin'), nullable=False)
    contact_mobile = Column(String(13), nullable=False)
    contact_email = Column(String(100), nullable=False)
    type = Column(Integer, nullable=False)
    balance = Column(Integer, nullable=True)
    remark = Column(String(200, u'utf8_bin'), nullable=False)
    create_at = Column(DateTime, nullable=False, server_default=FetchedValue())
    update_at = Column(DateTime)
    delete_at = Column(DateTime)

    @classmethod
    def get_one(cls, **fields: Dict[str, Any]) -> 'Company':
        return cls.query.filter_by(**fields).first()

    @classmethod
    def get_all(cls) -> List['Company']:
        return cls.query.all()
