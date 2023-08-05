from typing import Tuple

from qin_brick import Base
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import FetchedValue
from sqlalchemy import Integer
from sqlalchemy import String


class CompanyProduct(Base):
    __tablename__ = 'company_product'
    __bind_key__ = 'guard'

    id = Column(Integer, primary_key=True)
    service_name = Column(nullable=False, index=True)
    mode = Column(String(128), nullable=False)
    company_uuid = Column(nullable=False, index=True)
    type = Column(Integer, nullable=False, server_default=FetchedValue())
    status = Column(Integer)
    limit_day = Column(Integer, nullable=False)
    limit_total = Column(Integer, nullable=False)
    user_id = Column(nullable=False, index=True)
    price = Column(Integer, nullable=True)
    create_at = Column(DateTime, nullable=False, server_default=FetchedValue())
    update_at = Column(DateTime)
    delete_at = Column(DateTime)

    @classmethod
    def get_product_by_uuid(cls, company_uuid: str) -> Tuple:
        return cls.query(cls.service_name, cls.mode).filter_by(company_uuid=company_uuid).all()

    @classmethod
    def has_permission_for_product(cls, company_uuid: str, service: str) -> bool:
        return cls.query.filter_by(service_name=service, company_uuid=company_uuid).first() is not None
