from sqlalchemy import (
    Column,
    Index,
    Integer,
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

from . import BASE

#
# Note
#
class Note(BASE):
    __tablename__ = 'note'
    id         = Column(Integer, primary_key=True)
    subject    = Column(Text, nullable=False)
    message    = Column(Text, nullable=False)
    timestamp  = Column(DateTime, nullable=False)
    host_id    = Column(Integer, ForeignKey('host.id'))
    host       = relationship ("Host", backref="notes")

Index('u_note_index', Note.id, unique=True, mysql_length=255)
