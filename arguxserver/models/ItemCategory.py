"""ItemCategory module, containing ItemCategory model."""

from sqlalchemy import (
    Column,
    Index,
    Integer,
    Text
)

from . import BASE


# pylint: disable=too-few-public-methods
class ItemCategory(BASE):

    """ItemCategory class.

    Organise items in categories to make them easier to identify.
    """

    __tablename__ = 'item_category'
    id = Column(Integer, primary_key=True)  # pylint: disable=invalid-name
    name = Column(Text, nullable=False)

Index('u_itemcategory_name', ItemCategory.name, unique=True, mysql_length=255)
