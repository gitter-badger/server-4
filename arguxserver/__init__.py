from pyramid.config import Configurator

from pyramid.renderers import JSON

from sqlalchemy import engine_from_config

from .models import (
    DBSession,
    Base,
    )

from arguxserver import dao


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    settings['dao'] = dao
    config = Configurator(settings=settings)
    config.include('pyramid_chameleon')
    config.add_static_view('static', 'static', cache_max_age=3600)

    config.add_route('home',         '/')
    config.add_route('hosts',        '/host')
    config.add_route('host',         '/host/{host}')
    config.add_route('host_details', '/host/{host}/{action}')
    config.add_route('item',         '/host/{host}/item/{item}')
    config.add_route('item_details', '/host/{host}/item/{item}/{action}')

    config.add_route('dashboards',   '/dashboard')


    # REST 1.0 API
    config.add_route('rest_hosts_1',
            '/rest/1.0/host')
    config.add_route('rest_host_1',
            '/rest/1.0/host/{host}')
    config.add_route('rest_host_details_1',
            '/rest/1.0/host/{host}/details')

    config.add_route('rest_item_1',
            '/rest/1.0/host/{host}/item/{item}')
    config.add_route('rest_values_1',
            '/rest/1.0/host/{host}/item/{item}/values')

    config.add_route('rest_note_1',
            '/rest/1.0/note')

    config.add_route('rest_itemtype_details_1',
            '/rest/1.0/itemtype/{itemtype}/detail')
    config.add_route('rest_itemtype_detail_1',
            '/rest/1.0/itemtype/{itemtype}/detail/{id}')

    # Pretty-print JSON, useful for development.
    if (settings['rest.pretty_json'] == 'true'):
        config.add_renderer('json', JSON(indent=4))

    config.scan('.views')
    config.scan('.rest.views')
    return config.make_wsgi_app()
