"""Abstract BaseView class."""


# pylint: disable=too-few-public-methods
class BaseView(object):

    """BaseView class.

    Contains dao and request object.
    """

    def __init__(self, request):
        """Initialise BaseView."""
        self.request = request
        self.dao = request.registry.settings['dao']

