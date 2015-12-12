from arguxserver.models import (
    DBSession,
    Host,
    Note
    )


class NoteDAO(object):

    def getNotesForHost(self, host):
        n = DBSession.query(Note).filter(Note.host == host).order_by(Note.timestamp. desc())
        return n

    def createHostNote(self, host, subject, message, timestamp):
        n = Note(host=host, subject=subject,message=message, timestamp=timestamp)
        DBSession.add(n)
        return n
