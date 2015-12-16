# Package

from . import HostDAO
from . import NoteDAO
from . import ItemDAO

class DAO(object):

    def __init__(self):
        self.HOST_DAO = HostDAO
        self.ITEM_DAO = ItemDAO
        self.NOTE_DAO = NoteDAO
