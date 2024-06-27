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

from abc import ABC

from petace.network import NetParams, NetScheme, NetFactory
from petace.duet import VM
import petace.securenumpy as snp

from .process import Process


class PETAceTestException(Exception):

    def __init__(self, party, message) -> None:
        self.party = party
        self.message = message

    def __str__(self):
        return f"party {self.party} test failed: {self.message}"


def run_test(test_func):
    processes = []

    for i in range(2):
        p = Process(target=test_func, args=(i,))
        p.start()
        processes.append(p)
    for p in processes:
        p.join()

    for n, p in enumerate(processes):
        if p.exception:
            error, _ = p.exception
            p.terminate()
            raise PETAceTestException(n, error)


def init_network(party):
    net_params = NetParams()
    ip1 = "127.0.0.1"
    port1 = 8890
    ip2 = "127.0.0.1"
    port2 = 8891
    if party == 0:
        net_params.remote_addr = ip1
        net_params.remote_port = port1
        net_params.local_port = port2
    else:
        net_params.remote_addr = ip2
        net_params.remote_port = port2
        net_params.local_port = port1
    net = NetFactory.get_instance().build(NetScheme.SOCKET, net_params)
    return net


class NetworkTestBase(ABC):

    def run_test_all(self):
        run_test(self.run_process)

    def run_process(self, party):
        self.net = init_network(party)
        for method in dir(self):
            if method.startswith("test_"):
                getattr(self, method)(party)


def init_vm(party):
    net = init_network(party)

    duet = VM(net, party)
    return duet


class SnpTestBase(ABC):

    def run_test_all(self):
        run_test(self.run_process)

    def run_process(self, party):
        vm = init_vm(party)
        snp.set_vm(vm)
        for method in dir(self):
            if method.startswith("test_"):
                getattr(self, method)(vm.party_id())
