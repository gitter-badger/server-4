"""Module containing base class for all DAOs"""


# pylint: disable=too-few-public-methods
class BaseDAO:

    """BaseDAO class.

    Base class for all DAOs.
    """

    def __init__(self, session):
        """Initialise DAO."""
        self.db_session = session
