from sqlalchemy import (
    Column,
    Index,
    Integer,
    Text,
    ForeignKey,
    Boolean
    )

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    relationship
    )

from .ItemType import ItemType

from . import Base

#
# ItemTypeDetail
#
class ItemTypeDetail(Base):
    __tablename__ = 'itemtype_detail'
    id = Column(Integer, primary_key=True)
    itemtype_id = Column(Integer, ForeignKey('itemtype.id'), nullable=False)
    itemtype = relationship(ItemType, backref = 'details');
    name = Column(Text, nullable=False);
    rule = Column(Text, nullable=False);
 
Index('u_itemtypedetail_id_index', ItemTypeDetail.id, unique=True, mysql_length=255)
Index('u_itemtypedetail_itemtype_id_index', ItemTypeDetail.itemtype_id, mysql_length=255)
