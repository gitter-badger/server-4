from sqlalchemy import (
    Column,
    Index,
    Integer,
    Float,
    Text,
    DateTime,
    ForeignKey
    )

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    relationship
    )

from .. import Base

class FloatValue(Base):
    __tablename__ = 'history_float'
    id = Column(Integer, primary_key=True)
    value = Column(Float, nullable=True)
    timestamp = Column(DateTime, nullable=False)
    item_id = Column(Integer, ForeignKey('item.id'), nullable=False)
