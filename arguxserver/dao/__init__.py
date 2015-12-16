"""ArguxServer Data Access Objects."""

from . import (
    HostDAO,
    ItemDAO,
    NoteDAO
)


# pylint: disable=too-few-public-methods
class DAO(object):

    """Main DAO Class.

    This Class loads all modules containg the other DAO functions.
    """

    def __init__(self):
        self.host_dao = HostDAO
        self.item_dao = ItemDAO
        self.note_dao = NoteDAO

