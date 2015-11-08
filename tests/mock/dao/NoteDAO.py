class Note:

    def __init__(self, subject, body, timestamp):
        self.subject = subject
        self.body = body
        self.timestamp = timestamp

def createNote(subject, body, timestamp):
    n = Note(subject=subject,body=body, timestamp=timestamp)
    return n
