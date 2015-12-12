from arguxserver.models import (
    DB_SESSION,
    Note
    )


class NoteDAO(object):

    def get_notes_for_host(self, host):
        note = DB_SESSION.query(Note).filter(Note.host == host).order_by(Note.timestamp. desc())
        return note

    def create_hostNote(self, host, subject, message, timestamp):
        note = Note(host=host, subject=subject, message=message, timestamp=timestamp)
        DB_SESSION.add(note)
        return note
