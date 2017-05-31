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


class BindRNDCRequires(RelationBase):
    scope = scopes.UNIT

    # These remote data fields will be automatically mapped to accessors
    # with a basic documentation string provided.

    @hook('{requires:bind-rndc}-relation-joined')
    def joined(self):
        conv = self.conversation()
        conv.set_state('{relation_name}.connected')

    @hook('{requires:bind-rndc}-relation-changed')
    def changed(self):
        conv = self.conversation()
        conv.set_state('{relation_name}.connected')
        if self.data_complete():
            conv.set_state('{relation_name}.available')

    @hook('{requires:bind-rndc}-relation-{broken,departed}')
    def departed_or_broken(self):
        conv = self.conversation()
        conv.remove_state('{relation_name}.connected')
        conv.remove_state('{relation_name}.available')

    def data_complete(self):
        """Check if all information for a RNDC connection has been sent

        @returns boolean: True if all required data for connection is present
        """
        if self.rndc_info and all(self.rndc_info.values()):
            return True
        return False

    @property
    def rndc_info(self):
        """Get RNDC connection information from DNS Slave

        @returns dict: Return dict of RNDC connection information
        """
        for conv in self.conversations():
            data = {
                'algorithm': conv.get_remote('algorithm'),
                'secret': conv.get_remote('rndckey'),
            }
            if all(data.values()):
                return data
        return {}

    @property
    def algorithm(self):
        """Get algorith used to gen rndc secret from DNS Slave

        @returns str: Return algorith used to gen rndc secret
        """
        return self.rndc_info.get('algorithm')

    @property
    def rndckey(self):
        """Get rndc secret from DNS Slave

        @returns str: Return rndc secret
        """
        return self.rndc_info.get('secret')

    @property
    def private_address(self):
        """Get private address of unit in current relation context

        @returns str: Return ip address
        """
        conv = self.conversation()
        return conv.get_remote('private-address')

    def slave_ips(self):
        """Address information of DNS slaves

        @return list: List of dicts containing unit name and address
        """
        values = []
        for conv in self.conversations():
            values.append({
                # Unit scoped relation so only one unit per conversation.
                'unit': list(conv.units)[0],
                'address': conv.get_remote('private-address')})
        return values
