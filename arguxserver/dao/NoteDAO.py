from arguxserver.models import (
    DBSession,
    Host,
    Note,
    NoteMap
    )


def getNotesForHost(host):
    #c = DBSession.query(NoteMap).filter(NoteMap.host_id == host.id)
    return None

def createNote(subject, body, timestamp):
    n = Note(subject=subject,body=body, timestamp=timestamp)
    DBSession.add(n)
    return n

def mapNoteToHost(note, host):
    m = NoteMap(note_id=note.id, host_id = host.id)
    DBSession.add(m)
