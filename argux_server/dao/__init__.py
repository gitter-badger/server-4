"""ArguxServer Data Access Objects."""

from .ItemDAO import ItemDAO
from .HostDAO import HostDAO
from .NoteDAO import NoteDAO
from .TriggerDAO import TriggerDAO


# pylint: disable=too-few-public-methods
class DAO(object):

    """Main DAO Class.

    This Class loads all modules containg the other DAO functions.
    """

    def __init__(self, db_session):
        """Constructor function.

        Initialises public member DAO modules.
        """
        self.host_dao = HostDAO(db_session)
        self.item_dao = ItemDAO(db_session)
        self.note_dao = NoteDAO(db_session)
        self.trigger_dao = TriggerDAO(db_session)
