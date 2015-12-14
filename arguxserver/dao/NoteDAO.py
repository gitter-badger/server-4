from arguxserver.models import (
    DB_SESSION,
    Note
)


def get_notes_for_host(host):
    """Get notes for host."""
    note = DB_SESSION.query(Note).filter(Note.host == host).order_by(Note.timestamp. desc())
    return note


def create_host_note(host, subject, message, timestamp):
    """Create new note for host."""
    note = Note(host=host, subject=subject, message=message, timestamp=timestamp)
    DB_SESSION.add(note)
    return note
