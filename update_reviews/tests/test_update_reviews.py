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

import mock
from oslotest import mockpatch
import requests_mock

import update_reviews
from update_reviews.tests import base


class TestUpdateReviews(base.TestCase):

    def test_update_my_reviews(self):
        u_r = update_reviews.UpdateReviews(
            mock.sentinel.user, mock.sentinel.password)

        sample_reviews = [mock.sentinel.r1, mock.sentinel.r2]
        po = mockpatch.PatchObject(u_r, '_list_my_reviews',
                                   return_value=sample_reviews)
        list_my_reviews_mock = self.useFixture(po).mock

        update_review_mock = self.useFixture(
            mockpatch.PatchObject(u_r, '_update_review')).mock

        u_r.update_my_reviews()

        self.assertEqual(1, list_my_reviews_mock.call_count)
        exp_calls = [mock.call(mock.sentinel.r1), mock.call(mock.sentinel.r2)]
        self.assertEqual(exp_calls, update_review_mock.call_args_list)

    @requests_mock.mock()
    def test_list_my_reviews(self, m):
        u_r = update_reviews.UpdateReviews(
            mock.sentinel.user, mock.sentinel.password)

        sample_result = []

        gerrit_magic_prefix = ")]}'\n"
        sample_text = '%s%s' % (gerrit_magic_prefix, json.dumps(sample_result))
        m.get('https://review.openstack.org/a/changes/', text=sample_text)
        ret = u_r._list_my_reviews()
        self.assertEqual(sample_result, ret)
        exp_qs = {
            'n': ['2'],
            'q': ['project:openstack/oslo.config branch:master status:open '
                  'label:code-review=-2']}
        self.assertEqual(exp_qs, m.request_history[0].qs)
