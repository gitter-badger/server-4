import unittest

from pyramid import testing
from pyramid import request
from pyramid.registry import Registry

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker
)

from zope.sqlalchemy import ZopeTransactionExtension

from argux_server.rest.views.auth import RestAuthenticationViews

def _initTestingDB():
    from sqlalchemy import create_engine
    import transaction
    from argux_server.models import (
        DB_SESSION,
        BASE,
        ItemType,
        TriggerSeverity,
        HashMethod
        )
    from argux_server.dao.UserDAO import UserDAO

    engine = create_engine('sqlite://')
    BASE.metadata.create_all(engine)
    session = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
    session.configure(bind=engine)
    with transaction.manager:
        model = ItemType(name='int', description='Integer field')
        session.add(model)
        model = ItemType(name='float', description='Floating point')
        session.add(model)
        model = ItemType(name='text', description='Text')
        session.add(model)

        model = TriggerSeverity(level=1, key="info", name="Information")
        session.add(model)
        model = TriggerSeverity(level=2, key="warn", name="Warning")
        session.add(model)
        model = TriggerSeverity(level=3, key="crit", name="Critical")
        session.add(model)

        model = HashMethod(name='bcrypt', allowed=True)
        session.add(model)

        user_dao = UserDAO(session)
        user_dao.create_user('', 'admin', 'admin', hash_method='bcrypt')
        
    return session 

class RestAuthViewsTests(unittest.TestCase):

    def setUp(self):
        _initTestingDB()
        from argux_server import main
        settings = {
            'sqlalchemy.url': 'sqlite://',
            'session.secure_cookie': 'false',
            'rest.pretty_json': 'true'
        }
        app = main({}, **settings)
        from webtest import TestApp
        self.testapp = TestApp(app)

    def tearDown(self):
        del self.testapp

    def test_login(self):
        """

        """
        # r = request.Request.blank(
        #     path='/argux/rest/1.0/login')
        resp = self.testapp.post_json(
            '/rest/1.0/login',
            dict(username='admin',password='admin'))

        self.assertEquals(resp.status_int, 200)
