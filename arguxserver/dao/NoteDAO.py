from arguxserver.models import (
    DBSession,
    Host,
    Note
    )


def getNotesForHost(host):
    #c = DBSession.query(NoteMap).filter(NoteMap.host_id == host.id)
    return None

def createHostNote(host, subject, body, timestamp):
    n = Note(host=host, subject=subject,body=body, timestamp=timestamp)
    DBSession.add(n)
    return n
