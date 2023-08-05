from qin_brick import Base
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import FetchedValue
from sqlalchemy import Integer
from sqlalchemy import String


class CompanyRechargeJournal(Base):
    __tablename__ = "company_recharge_journal"
    __bind_key__ = 'guard'

    id = Column(Integer, primary_key=True)
    company_uuid = Column(String(128), nullable=False, comment="")
    recharge_order_sn = Column(String(128), nullable=True, comment="")
    real_money = Column(Integer, nullable=True, comment='')
    net_money = Column(Integer, nullable=True, comment="")
    pay_at = Column(DateTime, nullable=True, comment="")
    status = Column(Integer, nullable=True, comment="")
    pay_type = Column(String(64), nullable=True, comment="")
    create_at = Column(DateTime, nullable=False, server_default=FetchedValue())
    update_at = Column(DateTime)
    delete_at = Column(DateTime)
