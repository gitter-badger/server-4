"""Authentication REST Interface."""

from pyramid.view import (
    view_config,
    view_defaults,
)

from pyramid.security import (
    remember,
    forget,
    authenticated_userid
)

from pyramid.response import Response

from pyramid.httpexceptions import (
    HTTPBadRequest
)

import json

from . import RestView


@view_defaults(renderer='json')
class RestAuthenticationViews(RestView):

    @view_config(
        route_name='rest_login_1',
        request_method='POST',
    )
    def login_1_view(self):
        username = self.request.json_body.get('username', None)
        password = self.request.json_body.get('password', None)

        if username == password:
            self.request.session['username'] = username

            headers = remember(self.request, username)

            response = Response(
                content_type="application/json",
                body=json.dumps(
                    {
                        'status': 'success'
                    }))
            response.headerlist.extend(headers)
            response.headerlist.extend(
                [(
                   'X-CSRF-Token',
                    self.request.session.get_csrf_token()
                )])

            return response

        return HTTPBadRequest()
