from .database import Base
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, false, true
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text

class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, nullable=false, index=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='TRUE',nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))


class AccountsUser(Base):
    __tablename__ = 'accounts_users'

    id = Column(Integer, primary_key=True, nullable=false, index=True)
    email = Column(String, nullable=False, unique=True)
    username = Column(String, nullable=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))
