#!/usr/bin/env python

"""
NetData plugin for active users on Nextcloud servers.

Copyright (C) 2020 Arno Welzel

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
import xml.etree.ElementTree as ElementTree

# Basic plugin settings for netdata.
update_every = 5
priority = 60000
retries = 10

ORDER = ['users']

CHARTS = {
    'users': {
        'options': [None, 'Users active', 'users', 'Users', 'nextcloud.active_users', 'line'],
        'lines': [
            ['connected_users5min', '5 min', 'absolute'],
            ['connected_users1hour', '1 hour', 'absolute'],
            ['connected_users24hours', '24 hours', 'absolute'],
        ]
    },
}

class Service(UrlService):
    def __init__(self, configuration=None, name=None):
        UrlService.__init__(self, configuration=configuration, name=name)
        self.order = ORDER
        self.definitions = CHARTS
        self.user = self.configuration.get('user') 
        self.password = self.configuration.get('pass')
        self.url = self.configuration.get('url', 'http://localhost/ocs/v2.php/apps/serverinfo/api/v1/info')

    def check(self):
        self._manager = self._build_manager()

        data = self._get_data()

        if not data:
            return None

        return True
        
    def _get_data(self):
        data = dict()
        raw_data = self._get_raw_data()
        
        if not raw_data:
            return None
        tree = ElementTree.fromstring(raw_data);
        user5min = tree.find(".//activeUsers/last5minutes")
        user1hour = tree.find(".//activeUsers/last1hour")
        user24hours = tree.find(".//activeUsers/last24hours")
        data['connected_users5min'] = user5min.text
        data['connected_users1hour'] = user1hour.text
        data['connected_users24hours'] = user24hours.text
        
        return data or None
