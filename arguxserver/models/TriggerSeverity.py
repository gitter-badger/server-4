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

from . import Base

#
# TriggerSeverity
#
class TriggerSeverity(Base):
    __tablename__ = 'trigger_severity'
    id = Column(Integer, primary_key=True)
    key = Column(Text, nullable=False)
    name = Column(Text, nullable=False)
    level = Column(Integer, nullable=False)
 
Index('u_trigger_severity_id_index', TriggerSeverity.id, unique=True, mysql_length=255)
Index('u_trigger_severity_key_index', TriggerSeverity.key, unique=True, mysql_length=255)
Index('u_trigger_severity_name_index', TriggerSeverity.name, unique=True, mysql_length=255)
Index('u_trigger_severity_level_index', TriggerSeverity.level, unique=True, mysql_length=255)
