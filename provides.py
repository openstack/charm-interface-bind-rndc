#!/usr/bin/python
#
# Copyright 2016 Canonical Ltd
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

from charms.reactive import RelationBase
from charms.reactive import hook
from charms.reactive import scopes
from charms.reactive.bus import get_states

from charmhelpers.core import hookenv


class BindRNDCProvides(RelationBase):
    scope = scopes.UNIT

    @hook('{provides:bind-rndc}-relation-joined')
    def joined(self):
        conv = self.conversation()
        conv.set_state('{relation_name}.related')
        hookenv.log('States: {}'.format(get_states().keys()))

    @hook('{provides:bind-rndc}-relation-departed')
    def departed(self):
        conv = self.conversation()
        conv.remove_state('{relation_name}.related')

    def send_rndckey_info(self, rndckey, algorithm):
        for conv in self.conversations():
            conv.set_remote('rndckey', rndckey)
            conv.set_remote('algorithm', algorithm)

    def client_ips(self):
        ips = []
        for conv in self.conversations():
            ips.append(conv.get_remote('private-address'))
        return ips
