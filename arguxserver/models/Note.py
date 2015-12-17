"""Note module, containing Note models."""

from sqlalchemy import (
    Column,
    Index,
    Integer,
    Text,
    DateTime,
    ForeignKey
)

from sqlalchemy.orm import (
    relationship
)

from . import BASE


# pylint: disable=too-few-public-methods
class Note(BASE):

    """Note Model.

    Model for storing Host Notes.
    """

    __tablename__ = 'note'
    id = Column(Integer, primary_key=True)  # pylint: disable=invalid-name
    subject = Column(Text, nullable=False)
    message = Column(Text, nullable=False)
    timestamp = Column(DateTime, nullable=False)
    host_id = Column(Integer, ForeignKey('host.id'))
    host = relationship("Host", backref="notes")

Index('u_note_index', Note.id, unique=True, mysql_length=255)
