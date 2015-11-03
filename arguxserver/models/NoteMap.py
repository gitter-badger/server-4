from sqlalchemy import (
    Column,
    Index,
    Integer,
    Text,
    ForeignKey
    )

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    relationship
    )

from . import Base

#
# NoteMap
#
class NoteMap(Base):
    __tablename__ = 'note_map'
    id         = Column(Integer, primary_key=True)
    note_id    = Column(Integer, ForeignKey('note.id'), nullable=False)
    host_id    = Column(Integer, ForeignKey('host.id'), nullable=True)

Index('u_note_map_index', NoteMap.id, unique=True, mysql_length=255)
Index('u_note_map_note_id_index', NoteMap.note_id, unique=True, mysql_length=255)
Index('u_note_map_host_id_index', NoteMap.host_id, mysql_length=255)

