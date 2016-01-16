#!/usr/bin/python
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

from charms.reactive import RelationBase
from charms.reactive import hook
from charms.reactive import scopes


class BindRNDCRequires(RelationBase):
    scope = scopes.GLOBAL

    # These remote data fields will be automatically mapped to accessors
    # with a basic documentation string provided.
    auto_accessors = ['algorithm', 'secret']

    @hook('{requires:bind-rndc}-relation-joined')
    def joined(self):
        self.set_state('{relation_name}.connected')

    @hook('{requires:bind-rndc}-relation-changed')
    def changed(self):
        self.set_state('{relation_name}.connected')
        if self.data_complete():
            self.set_state('{relation_name}.available')

    @hook('{requires:bind-rndc}-relation-{broken,departed}')
    def departed_or_broken(self):
        self.remove_state('{relation_name}.connected')
        if not self.data_complete():
            self.remove_state('{relation_name}.available')

    def data_complete(self):
        """
        Get the connection string, if available, or None.
        """
        data = {
            'algorithm': self.algorithm(),
            'secret': self.secret(),
        }
        if all(data.values()):
            return True
        return False
