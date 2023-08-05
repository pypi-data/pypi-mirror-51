# -*- coding: utf-8 -*-
"""
如果在 Flask 中想要使用 model 模块，可以做如下配置：

对 Sqlalchemy 进行相关配置：
DB_CONF: Dict[str, Any] = {
    'SQLALCHEMY_DATABASE_URI':
        f'mysql+pymysql://root:{PROD_DB["password"]}@{PROD_DB["host"]}/{PROD_DB["inner_platform"]}?charset=utf8',
    'SQLALCHEMY_BINDS': {
        'guard': f'mysql+pymysql://root:{PROD_DB["password"]}@{PROD_DB["host"]}/{PROD_DB["database"]}?charset=utf8',
        'default': f'mysql+pymysql://root:{PROD_DB["password"]}@{PROD_DB["host"]}'
        f'/{PROD_DB["inner_platform"]}?charset=utf8',
    },
    'SQLALCHEMY_ECHO': True,
    'SQLALCHEMY_COMMIT_ON_TEARDOWN':False,
    # 这个配置一般都是不推荐的，但是如果不配置的话，运行一段时间后会抛出异常。
    'SQLALCHEMY_TRACK_MODIFICATIONS': True
}

初始化：
from flask_sqlalchemy import SQLAlchemy
app.config.from_mapping(DB_CONF)
SQLAlchemy().init_app(app)

调用, 直接调用相关方法就 ok：
CompanyProduct.has_permission_for_product


销毁生命周期--- 如果配置了 SQLALCHEMY_TRACK_MODIFICATIONS, 这个可以不配置。
@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()
"""
# from typing import Any
#
# from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy import create_engine
# from sqlalchemy.engine import Engine
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import scoped_session
# from sqlalchemy.orm import sessionmaker
#
# # this is used to create all tables auto
# # Base.metadata.create_all(engine)
# SQLALCHEMY_POOL_RECYCLE = 10
# db = SQLAlchemy(use_native_unicode='utf8')
# Base = declarative_base()
#
# DBSession = sessionmaker()
# Scoped = scoped_session(DBSession)
#
#
# def generate_engine(url: str, pool_recycle: int = SQLALCHEMY_POOL_RECYCLE) -> Engine:
#     return create_engine(url, encoding='utf-8', echo=True, pool_recycle=pool_recycle)
#
#
# def call_procedure(url: str, procedure_name: str, *args: Any) -> None:
#     """
#
#     :param url:
#     :param procedure_name: just procedure name not call procedure_name
#     :param args:
#     :return:
#     """
#     connection = generate_engine(url).raw_connection()
#     cursor = connection.cursor()
#     try:
#         s = cursor.callproc(procedure_name, args=args)
#         print(s)
#         connection.commit()
#     except Exception as e:
#         connection.rollback()
#     finally:
#         cursor.close()
#         connection.close()


from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# engine = create_engine('sqlite:////tmp/test.db', convert_unicode=True)
# db_session = scoped_session(sessionmaker(autocommit=False,
#                                          autoflush=False,
#                                          bind=engine))
Base = declarative_base()
# Base.query = db_session.query_property()
