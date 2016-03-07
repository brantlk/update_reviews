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
import sys

import update_reviews


def updating_review_cb(r):
    print('Updating %s in %s' % (r['change_id'], r['project']))


def main():
    user = sys.argv[1]
    password = sys.argv[2]
    project = sys.argv[3]
    print('Running...')
    u_r = update_reviews.UpdateReviews(user, password, project,
                                       updating_review_cb=updating_review_cb)
    print(json.dumps(u_r._list_my_reviews(), indent=4))
    print('Done')


main()
