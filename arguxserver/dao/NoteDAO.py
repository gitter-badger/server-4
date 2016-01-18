"""Data Access Object class for handling Notes."""

from arguxserver.models import (
    Note
)


class NoteDAO():

    """Note DAO.

    Data Access Object for handling Notes.
    """

    def __init__(self, session):
        self.db_session = session

    def get_notes_for_host(self, host):
        """Get notes for host."""
        note = self.db_session.query(Note)\
            .filter(Note.host == host)\
            .order_by(Note.timestamp.desc())\
            .all()

        return note


    def create_note_for_host(self, host, subject, message, timestamp):
        """Create new note for host."""
        note = Note(host=host, subject=subject, message=message, timestamp=timestamp)
        self.db_session.add(note)
        return note
