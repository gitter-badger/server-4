"""ArguxServer Module."""

from pyramid.authentication import SessionAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy

from pyramid.config import Configurator

from pyramid.renderers import JSON

from pyramid.session import SignedCookieSessionFactory

from pyramid.security import (
    ALL_PERMISSIONS,
    Everyone,
    Authenticated,
    Allow
)

from sqlalchemy import engine_from_config

from .models import (
    DB_SESSION,
    BASE,
)

from arguxserver import dao

from arguxserver.trigger import TriggerWorker


# MAP GROUPS TO PERMISSIONS
class RootFactory(object):

    """ RootFactory:

    __acl__: base ACL
    """

    __acl__ = [
        (Allow, 'g:admin', ALL_PERMISSIONS),
        (Allow, Authenticated, 'view'),
        (Allow, Everyone, 'koffie')
    ]

    def __init__(self, request):
        """Initialize RootFactory."""
        self.request = request


# pylint: disable=unused-argument
def main(global_config, **settings):
    """Return a Pyramid WSGI application."""
    engine = engine_from_config(settings, 'sqlalchemy.')
    DB_SESSION.configure(bind=engine)
    BASE.metadata.bind = engine
    settings['dao'] = dao.DAO(DB_SESSION)

    factory = SignedCookieSessionFactory('SEECREET')
    authentication_policy = SessionAuthenticationPolicy()
    authorization_policy = ACLAuthorizationPolicy()

    config = Configurator(
        settings=settings,
        root_factory=RootFactory
    )
    config.set_session_factory(factory)
    config.set_authentication_policy(authentication_policy)
    config.set_authorization_policy(authorization_policy)

    config.include('pyramid_chameleon')
    config.add_static_view('static', 'static', cache_max_age=3600)

    config.add_route('home', '/')
    config.add_route('host_overview_default', '/hosts')
    config.add_route('host_overview', '/hosts/{action}')
    config.add_route('host_default', '/host/{host}')
    config.add_route('host', '/host/{host}/{action}')
    config.add_route('item', '/host/{host}/item/{item}')
    config.add_route('item_details', '/host/{host}/item/{item}/{action}')
    config.add_route('login', '/login')
    config.add_route('logout', '/logout')

    config.add_route('dashboards', '/dashboard')

    # REST 1.0 API
    config.add_route('rest_login_1',
                     '/rest/1.0/login')
    config.add_route('rest_logout_1',
                     '/rest/1.0/logout')
    config.add_route('rest_hosts_1',
                     '/rest/1.0/host')
    config.add_route('rest_host_1',
                     '/rest/1.0/host/{host}')
    config.add_route('rest_host_details_1',
                     '/rest/1.0/host/{host}/details')

    config.add_route('rest_item_1',
                     '/rest/1.0/host/{host}/item/{item}')
    config.add_route('rest_item_details_1',
                     '/rest/1.0/host/{host}/item/{item}/details')
    config.add_route('rest_item_values_1',
                     '/rest/1.0/host/{host}/item/{item}/values')
    config.add_route('rest_triggers_1',
                     '/rest/1.0/host/{host}/item/{item}/trigger')
    config.add_route('rest_trigger_validate_1',
                     '/rest/1.0/host/{host}/item/{item}/trigger/validate')
    config.add_route('rest_trigger_1',
                     '/rest/1.0/host/{host}/item/{item}/trigger/{id}')

    config.add_route('rest_note_1',
                     '/rest/1.0/note')

    config.add_route('rest_itemtype_details_1',
                     '/rest/1.0/itemtype/{itemtype}/detail')
    config.add_route('rest_itemtype_detail_1',
                     '/rest/1.0/itemtype/{itemtype}/detail/{id}')

    # Pretty-print JSON, useful for development.
    if settings['rest.pretty_json'] == 'true':
        config.add_renderer('json', JSON(indent=4))

    config.scan('.views')
    config.scan('.rest.views')

    worker = TriggerWorker()
    worker.start()

    return config.make_wsgi_app()
