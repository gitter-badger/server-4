from sqlalchemy import (
    Column,
    Index,
    Integer,
    Text,
    ForeignKey,
)

from sqlalchemy.orm import (
    scoped_session,
    relationship
)

from . import BASE


# pylint: disable=too-few-public-methods
class TriggerSeverity(BASE):

    """Trigger Severity Class.

    List of severity-values in the database.

    eg.
      - warn
      - crit
    """

    __tablename__ = 'trigger_severity'
    id = Column(Integer, primary_key=True)  # pylint: disable=invalid-name
    key = Column(Text, nullable=False)
    name = Column(Text, nullable=False)
    level = Column(Integer, nullable=False)

Index('u_trigger_severity_id_index', TriggerSeverity.id, unique=True, mysql_length=255)
Index('u_trigger_severity_key_index', TriggerSeverity.key, unique=True, mysql_length=255)
Index('u_trigger_severity_name_index', TriggerSeverity.name, unique=True, mysql_length=255)
Index('u_trigger_severity_level_index', TriggerSeverity.level, unique=True, mysql_length=255)
