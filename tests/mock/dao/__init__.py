# Package

from . import HostDAO
from . import NoteDAO
from . import ItemDAO

class DAO(object):

    def __init__(self):
        self.host_dao = HostDAO
        self.item_dao = ItemDAO
        self.note_dao = NoteDAO
