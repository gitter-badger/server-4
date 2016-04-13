"""ICMPMonitor module."""

from threading import (
    Thread
)

from sqlalchemy.orm import (
    sessionmaker
)

from argux_server.dao import DAO
from argux_server.models import DB_SESSION


class AbstractMonitor(Thread):

    """AbstractMonitor class.

    Abstract Monitor class for all monitor threads.
    """

    def __init__(self, settings):
        """Initialise AbstractMonitor.

        This constructor builds a DAO and a Session object.
        This will generate warnings when running on SQLite since
        the session-object is created in the parent thread but used inside a child.
        """
        super(AbstractMonitor, self).__init__()
        self.daemon = True

        self.session = DB_SESSION

        self.dao = DAO(self.session)

    # pylint: disable=no-self-use
    def run(self):
        """Run placeholder."""
        raise NotImplementedError

    # pylint: disable=no-self-use
    def stop(self):
        """Stop placeholder."""
        return

    @classmethod
    def validate_options(cls, options):
        raise NotImplementedError
