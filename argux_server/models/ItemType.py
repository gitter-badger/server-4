"""ItemType model."""

from sqlalchemy import (
    Column,
    Index,
    Integer,
    Text,
)

from . import BASE


# pylint: disable=too-few-public-methods
class ItemType(BASE):

    """ItemType is a datatype of an Item.

    For every ItemType there should be a Trigger and Value implementation.
    """

    __tablename__ = 'itemtype'
    id = Column(Integer, primary_key=True)  # pylint: disable=invalid-name
    name = Column(Text, nullable=False)
    description = Column(Text, nullable=False)

Index('u_itemtype_name', ItemType.name, unique=True, mysql_length=255)
