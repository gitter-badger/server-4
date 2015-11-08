from arguxserver.models import (
    DBSession,
    Host,
    Note
    )


def getNotesForHost(host):
    n = DBSession.query(Note).filter(Note.host == host).order_by(Note.timestamp. desc())
    return n

def createHostNote(host, subject, message, timestamp):
    n = Note(host=host, subject=subject,message=message, timestamp=timestamp)
    DBSession.add(n)
    return n
