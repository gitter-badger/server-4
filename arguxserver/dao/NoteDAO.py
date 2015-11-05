from arguxserver.models import (
    DBSession,
    Host,
    Note
    )


def getNotesForHost(host):
    n = DBSession.query(Note).filter(Note.host == host)
    return n

def createHostNote(host, subject, body, timestamp):
    n = Note(host=host, subject=subject,body=body, timestamp=timestamp)
    DBSession.add(n)
    return n
