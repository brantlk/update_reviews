# -*- coding: utf-8 -*-

# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import json

import pbr.version
import requests
from requests import auth


__version__ = pbr.version.VersionInfo(
    'update_reviews').version_string()


def list_my_reviews(user, password):
    url = 'https://review.openstack.org/a/changes/'
    params = ('q=project:openstack/oslo.config+branch:master+status:open+'
              'label:Code-Review=-2&n=2')
    auth_ = auth.HTTPDigestAuth(user, password)
    r = requests.get(url, params=params, auth=auth_)
    r.raise_for_status()

    # Note that the result is not JSON, it's got a leading line that needs to
    # be removed first.
    res_text = r.text
    (dummy_magic_prefix, dummy_nl, res_json) = res_text.partition('\n')
    return json.loads(res_json)


def update_review(r):
    print(r)  # FIXME: implement.


def update_my_reviews(user, password):
    for r in list_my_reviews(user, password):
        update_review(r)
