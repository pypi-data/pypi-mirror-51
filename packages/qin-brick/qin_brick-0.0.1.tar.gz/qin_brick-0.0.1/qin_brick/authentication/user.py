from nezha.env import filter_locals
from qin_brick import Base
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import FetchedValue
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    uuid = Column(String(64), nullable=False, unique=True)
    role_uuid = Column(String(64), nullable=False)
    username = Column(String(32, u'utf8_bin'), nullable=False, unique=True)
    password = Column(String(128), nullable=False)
    email = Column(String(128), nullable=False, unique=True)
    phone = Column(String(128), nullable=False, unique=True)
    real_name = Column(String(128), nullable=False)
    company_name = Column(String(128), nullable=False)
    guard_uuid = Column(String(64), nullable=False)
    company_address = Column(String(128), nullable=False)
    business_desc = Column(Text, nullable=False, comment='公司业务描述')
    status = Column(Integer, nullable=False)
    remark = Column(String(200, u'utf8_bin'), nullable=False)
    last_login_time = Column(DateTime, nullable=False)
    update_at = Column(DateTime, nullable=False)
    create_at = Column(DateTime, nullable=False, server_default=FetchedValue())

    @staticmethod
    def generate_hash_password(password: str, salt: str) -> str:
        return ''

    @classmethod
    def get_role(cls, username: str = '', email: str = '', phone: str = '') -> str:
        variables = list(filter_locals(locals(), exclude_keys=('url', 'cls')))
        if len(variables) > 1:
            raise ValueError(f'variables {variables} is unexpected')
        key, value = variables[0]
        print('key, value', key, value)
        result = cls.query.filter(key == value).first()
        return result.role if result else ''
