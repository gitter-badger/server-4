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

# pylint: disable=too-few-public-methods
class HistoryGraphItems(BASE):

    """
    HistoryGraphItem class.

    Model for storing HistoryGraph - Item relationship details.
    """

    __tablename__ = 'history_graph_items'
    id = Column(Integer, primary_key=True)  # pylint: disable=invalid-name
    history_graph_id = Column(Integer, ForeignKey('history_graph.id'), nullable=False)
    history_graph = relationship(HistoryGraph, backref='items')
    item_id = Column(Integer, ForeignKey('item.id'))
