# Copyright 2023 TikTok Pte. Ltd.
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

from petace.setops import PSI, PJC
from petace.setops import PSIScheme, PJCScheme
from ..utils import NetworkTestBase


class TestSetops(NetworkTestBase):

    def test_ecdh_psi(self, party):
        data = []
        sender_obtain_result = False
        if party == 0:
            data = ["1", "2", "3"]
            sender_obtain_result = True
        else:
            data = ["2", "3"]
        psi = PSI(self.net, party, PSIScheme.ECDH_PSI)
        ret = psi.process(data, sender_obtain_result)
        if party == 0:
            assert ret == ["2", "3"]

    def test_kkrt_psi(self, party):
        data = []
        sender_obtain_result = False
        if party == 0:
            data = ["1", "2", "3"]
            sender_obtain_result = True
        else:
            data = ["2", "3"]
        psi = PSI(self.net, party, PSIScheme.KKRT_PSI)
        ret = psi.process(data, sender_obtain_result)
        if party == 0:
            assert ret == ["2", "3"]

    def test_circuit_psi(self, party):
        keys = []
        features = [[]]
        if party == 0:
            keys = ["1", "2", "3"]
            features = [[1, 2, 3]]
        else:
            keys = ["2", "3", "4"]
            features = [[5, 7, 9]]
        pjc = PJC(self.net, party, PJCScheme.CIRCUIT_PSI)
        _ = pjc.process(keys, features)
