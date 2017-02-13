#!/usr/bin/env python3
#
# Copyright 2017 Peter Schmidt
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
# ------ START CONFIG --------------------------------------------------------

# Dictionary with username and a list of devices for each user.
devices = {'peter': ['android-abcdefgh', 'pta-x240l'],
           'astrid': ['android-123456789'],
           }

# Dictionary username and ISE of the system variable. Lookup the ISE (ise_id)
# here: http://homematic-ccu2/config/xmlapi/sysvarlist.cgi
presencevars = {'peter': 1903,
                'astrid': 1902,
                }

# Username and password for Unifi controller. No write access needed.
unifi_login = {'username': 'foo', 'password': 'bar'}

# Host:Port of UniFi controler
unifi = 'unifi:8443'

# Hostname of the Homematic CCU2
ccu2 = 'homematic-ccu2'


# ------ END CONFIG ---------------------------------------------------------
# Suppress SSL warning caused by the self signed certificate of the controller
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
isHere = []

req = requests.Session()

# Login to the controller
r = req.post("https://{0}/api/login".format(unifi), json=unifi_login, verify=False, headers={'referer': "https://{0}/login".format(unifi)})

if r.status_code == 200:
    # Get a list of all connected clients
    r = req.post("https://{0}/api/s/default/stat/sta/".format(unifi), verify=False, headers={'referer': "https://{0}/login".format(unifi)})
    if r.status_code == 200:
        json = r.json()
        for x in json['data']:
            for username, devicelist in devices.items():
                if x['hostname'] in devicelist:
                    isHere.append(username)

    for user, ise in presencevars.items():
        value = '1' if user in isHere else '0'
        print('{0} is {1}.'.format(user, 'online' if user in isHere else 'offline'))

        url = 'http://{0}/config/xmlapi/statechange.cgi?ise_id={1}&new_value={2}'
        req.get(url.format(ccu2, ise, value))
else:
    print("Login to UniFi controller failed.")
