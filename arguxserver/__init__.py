from pyramid.config import Configurator

from pyramid.renderers import JSON

from sqlalchemy import engine_from_config

from .models import (
    DBSession,
    Base,
    )


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    config = Configurator(settings=settings)
    config.include('pyramid_chameleon')
    config.add_static_view('static', 'static', cache_max_age=3600)

    config.add_route('home',         '/')
    config.add_route('hosts',        '/host')
    config.add_route('host',         '/host/{host}')
    config.add_route('item_details', '/host/{host}/item/{item}/details')
    config.add_route('host_details', '/host/{host}/{action}')

    config.add_route('dashboards',   '/dashboard')

    config.add_route('hosts_1',   '/argux/rest/1.0/host')
    config.add_route('host_1',    '/argux/rest/1.0/host/{host}')
    config.add_route('item_1',    '/argux/rest/1.0/host/{host}/item/{item}')
    config.add_route('values_1',  '/argux/rest/1.0/host/{host}/item/{item}/values')
    config.add_route('host_details_1', '/argux/rest/1.0/host/{host}/details')

    config.add_route('note_1',   '/argux/rest/1.0/note')

    # Pretty-print JSON, useful for development.
    if (settings['rest.pretty_json'] == 'true'):
        config.add_renderer('json', JSON(indent=4))

    config.scan('.views')
    config.scan('.rest.views')
    return config.make_wsgi_app()
