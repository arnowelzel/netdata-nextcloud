#!/usr/bin/env python

"""
NetData plugin for active users on Nextcloud servers.

Copyright (C) 2020-2021 Arno Welzel

With contributions by Luca Olivetti and others

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

from bases.FrameworkServices.UrlService import UrlService
from json import loads

# Basic plugin settings for netdata.
update_every = 5
priority = 60000
retries = 10

ORDER = ['users',
         'files',
         'storage',
         'shares',
         'apps'
         ]

CHARTS = {
    'users': {
        'options': [None, 'Users active', 'users', 'Users', 'nextcloud.active_users', 'line'],
        'lines': [
            ['num_users', 'total', 'absolute'],
            ['last5minutes', '5 min', 'absolute'],
            ['last1hour', '1 hour', 'absolute'],
            ['last24hours', '24 hours', 'absolute'],
        ]
    },
    'files': {
        'options': [None, 'Files', 'files', 'Files', 'nextcloud.files', 'line'],
        'lines': [
            ['num_files', 'files', 'absolute'],
        ]
    },
    'storage': {
        'options': [None, 'Storage', 'storage', 'Storage', 'nextcloud.storage', 'stacked'],
        'lines': [
            ['num_storages_local', 'storages local', 'absolute'],
            ['num_storages_home', 'storages home', 'absolute'],
            ['num_storages_other', 'storages other', 'absolute'],
        ]
    },
    'shares': {
        'options': [None, 'Shares', 'shares', 'Shares', 'nextcloud.shares', 'line'],
        'lines': [
            ['num_shares', 'shares', 'absolute'],
            ['num_shares_user', 'shares user', 'absolute'],
            ['num_shares_groups', 'shares groups', 'absolute'],
            ['num_shares_link', 'shares link', 'absolute'],
            ['num_shares_link_no_password', 'shares link no password', 'absolute'],
            ['num_fed_shares_sent', 'fed shares sent', 'absolute'],
            ['num_fed_shares_received', 'fed shares received', 'absolute'],
        ]
    },
    'apps': {
        'options': [None, 'Apps', 'apps', 'Apps', 'nextcloud.apps', 'line'],
        'lines': [
            ['num_installed', 'num_installed', 'absolute'],
            ['num_updates_available', 'num_updates_available', 'absolute'],
        ]
    }
}


class Service(UrlService):
    def __init__(self, configuration=None, name=None):
        UrlService.__init__(self, configuration=configuration, name=name)
        self.order = ORDER
        self.definitions = CHARTS
        self.user = self.configuration.get('user')
        self.password = self.configuration.get('pass')
        self.url = self.configuration.get(
            'url', 'http://localhost')+'/ocs/v2.php/apps/serverinfo/api/v1/info?format=json'

    def check(self):
        self._manager = self._build_manager()

        data = self._get_data()

        if not data:
            return None

        return True

    def _get_data(self):
        raw_data = self._get_raw_data()

        if not raw_data:
            return None

        try:
            j = loads(raw_data)
            data = j['ocs']['data']['activeUsers']
            data.update(j['ocs']['data']['nextcloud']['storage'])
            data.update(j['ocs']['data']['nextcloud']['shares'])
            data.update(j['ocs']['data']['nextcloud']['system']['apps'])
            return data
        except ValueError:
            self.error('received data is not in json format')
        except KeyError:
            self.error('missing key in received data')

        return None
