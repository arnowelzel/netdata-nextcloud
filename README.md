# Nexctloud netdata Plugin

This is a [netdata](https://github.com/firehol/netdata/) plugin that polls
the number of active users from a Nexctloud server.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see http://www.gnu.org/licenses/.

## Installation

With your default netdata installation copy the nextcloud.chart.py script to
`/usr/libexec/netdata/python.d/` and the nextcloud.conf config file to
`/etc/netdata/python.d/`. The location of these directories may vary depending
on your distribution. Read your given release of netdata for more information.

Log in as aminidstator in Nextcloud and create a new app password for netdata.

Edit the config file to set the Nextcloud API URL, user name and app password.

Restart netdata to activate the plugin after you have made these changes.

To disable the Nextcloud plugin, edit `/etc/netdata/python.d.conf` and add
`nextcloud: no`.

## Version History

- v0.1 - Initial release
