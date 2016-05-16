"""HistoryGraph Module, containing HistoryGraph model."""

from sqlalchemy import (
    Column,
    Index,
    Integer,
    Float,
    Text,
    ForeignKey,
    Boolean
)

from sqlalchemy.orm import (
    relationship
)

from . import BASE

# pylint: disable=too-few-public-methods
class HistoryGraph(BASE):

    """
    HistoryGraph class.

    Model for storing HistoryGraph details.
    """

    __tablename__ = 'history_graph'
    id = Column(Integer, primary_key=True)  # pylint: disable=invalid-name
    name = Column(Text, nullable=False)
    suggested_min = Column(Float, nullable=True, default=None)
    suggested_max = Column(Float, nullable=True, default=None)
