"""MetricPrefix Module, containing MetricPrefix preferences of a Unit."""

from sqlalchemy import (
    Column,
    Index,
    Integer,
    Text,
    ForeignKey,
    Boolean
)

from sqlalchemy.orm import (
    relationship
)

from . import BASE

# pylint: disable=too-few-public-methods
class MetricPrefix(BASE):

    """
    MetricPrefix class.

    Model for storing MetricPrefixes.

    It has indicators to determine which prefixes are to be used for a unit.
    """

    __tablename__ = 'metric_prefix'
    id = Column(Integer, primary_key=True)  # pylint: disable=invalid-name
    unit = relationship("Unit", uselist=False, back_populates="metric_prefix")
    exa = Column(Boolean, default=False, nullable=False)   # 1.000.000.000.000.000.000
    peta = Column(Boolean, default=False, nullable=False)  # 1.000.000.000.000.000
    tera = Column(Boolean, default=False, nullable=False)  # 1.000.000.000.000
    giga = Column(Boolean, default=False, nullable=False)  # 1.000.000.000
    mega = Column(Boolean, default=False, nullable=False)  # 1.000.000
    kilo = Column(Boolean, default=False, nullable=False)  # 1.000
    hecto = Column(Boolean, default=False, nullable=False) # 100 
    deca = Column(Boolean, default=False, nullable=False)  # 10
    ####
    deci = Column(Boolean, default=False, nullable=False)  # 0,1
    centi = Column(Boolean, default=False, nullable=False) # 0,01
    milli = Column(Boolean, default=False, nullable=False) # 0,001
    micro = Column(Boolean, default=False, nullable=False) # 0,000 001
    nano = Column(Boolean, default=False, nullable=False)  # 0,000 000 001
    pico = Column(Boolean, default=False, nullable=False)  # 0,000 000 000 001
    femto = Column(Boolean, default=False, nullable=False) # 0,000 000 000 000 001
    atto = Column(Boolean, default=False, nullable=False)  # 0,000 000 000 000 000 001
