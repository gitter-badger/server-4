# package

class RestView:

    def __init__(self, request):
        self.request = request
        self.dao = request.registry.settings['dao']
