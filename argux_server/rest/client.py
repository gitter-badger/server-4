"""Argux REST client for Argux Server."""

import json
import requests

from requests.exceptions import (
    ConnectionError,
    HTTPError,
)

from argux_server.models.Host import Host


class RESTClient:

    """RESTClient.

    Class used to interact with ArguxServer
    """

    def __init__(self, base_url, username, secret):
        """Initialise RESTClient.

        Arguments:
            base_url:   base-url of argux-server, eg:
                        https://argux-server:port/
        """
        self.base_url = base_url
        self.username = username
        self.secret = secret
        self.cookies = {}
        self.headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }

    def __login(self):
        payload = {
            'username': self.username,
            'password': self.secret
        }
        try:
            response = requests.post(
                self.base_url+'/rest/1.0/login',
                headers=self.headers,
                data=json.dumps(payload))

            self.cookies['argux_server'] = response.cookies['argux_server']
            self.headers['X-Csrf-token'] = response.headers['X-Csrf-token']
        except ConnectionError as e:
            print(e)


    def get_hosts(self):

        self.__login()

        try:
            response = requests.get(
                self.base_url+'/rest/1.0/host',
                cookies = self.cookies,
                headers = self.headers)
        except ConnectionError as e:
            raise e
        except HTTPError as e:
            raise e

        json_response = response.json()
        if json_response is None:
            raise ValueError('Invalid Response, could not decode JSON')
        if not 'hosts' in json_response:
            raise ValueError('Invalid Response, missing \'hosts\' attribute')

        hosts = []

        for json_host in json_response['hosts']:
            if 'name' in json_host:
                hosts.append(Host(name=json_host['name']))

        return hosts

    def create_item(self, host, item):

        self.__login()

        payload = {
            'name': item.name,
            'type': item.item_type,
            'description': item.description,
            'category': item.category,
        }
        try:
            response = requests.post(
                self.base_url+'/rest/1.0/host/'+host+'/item/'+item.key,
                cookies=self.cookies,
                headers=self.headers,
                data=json.dumps(payload))
        except ConnectionError as e:
            raise e
        except HTTPError as e:
            raise e

        return
