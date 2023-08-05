from typing import List

from qin_brick import Base
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import FetchedValue
from sqlalchemy import Integer
from sqlalchemy import String


class RolePermission(Base):
    __tablename__ = 'role_permission'
    permission_can = '0'
    status_active = 0

    id = Column(Integer, primary_key=True)
    uuid = Column(String(64), nullable=False, unique=True)
    role_uuid = Column(String(64, u'utf8_bin'), nullable=False)
    block_uuid = Column(String(64, u'utf8_bin'), nullable=False)
    # permission 0 ok, 1 forbidden
    permission = Column(String(64, u'utf8_bin'), nullable=False)
    # status = 0 active, 1 discard
    status = Column(Integer, nullable=False)
    remark = Column(String(200, u'utf8_bin'), nullable=False)
    update_at = Column(DateTime, nullable=False)
    create_at = Column(DateTime, nullable=False, server_default=FetchedValue())

    @classmethod
    def get_all_companies(cls) -> List['RolePermission']:
        return cls.query.all()

    @classmethod
    def the_role_can_do(cls, role_uuid: str, block_uuid: str) -> bool:
        record: RolePermission = cls.query.filter_by(role_uuid=role_uuid, block_uuid=block_uuid).first()
        if not record:
            return False
        return record.permission == cls.permission_can and record.status == cls.status_active
