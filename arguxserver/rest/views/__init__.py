"""Abstract RestView class."""


# pylint: disable=too-few-public-methods
class RestView(object):

    """RestView class.

    Contains dao and request object.
    """

    def __init__(self, request):
        """Initialise RestView."""
        self.request = request
        self.dao = request.registry.settings['dao']
