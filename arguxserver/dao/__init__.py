"""
ArguxServer Data Access Objects.

"""

from .HostDAO import HostDAO
from .ItemDAO import ItemDAO
from .NoteDAO import NoteDAO

HOST_DAO = HostDAO()

ITEM_DAO = ItemDAO()

NOTE_DAO = NoteDAO()
