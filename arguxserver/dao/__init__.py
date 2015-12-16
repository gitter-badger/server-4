"""ArguxServer Data Access Objects."""

from . import (
    HostDAO,
    ItemDAO,
    NoteDAO
)

class DAO(object):

    def __init__(self):
        self.HOST_DAO = HostDAO
        self.ITEM_DAO = ItemDAO
        self.NOTE_DAO = NoteDAO

