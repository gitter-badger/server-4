from arguxserver.models import (
    DB_SESSION,
    Host,
    Note
    )


class NoteDAO(object):

    def getNotesForHost(self, host):
        n = DB_SESSION.query(Note).filter(Note.host == host).order_by(Note.timestamp. desc())
        return n

    def createHostNote(self, host, subject, message, timestamp):
        n = Note(host=host, subject=subject,message=message, timestamp=timestamp)
        DB_SESSION.add(n)
        return n
