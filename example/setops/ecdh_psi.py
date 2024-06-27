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

from petace.setops import PSI, PSIScheme
from petace.network import NetParams, NetScheme, NetFactory

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='PETAce-Duet demo.')
    parser.add_argument("-p", "--party", type=int, help="which party")
    parser.add_argument("--port0", type=int, help="port of party 0, defalut 8089", default=8089)
    parser.add_argument("--port1", type=int, help="port of party 1, defalut 8090", default=8090)
    parser.add_argument("--host", type=str, help="host of this party", default="127.0.0.1")

    # 解析命令行参数
    args = parser.parse_args()
    party = args.party
    port0 = args.port0
    port1 = args.port1
    host = args.host
    obtain_result = False
    data = []

    net_params = NetParams()
    if party == 0:
        net_params.remote_addr = host
        net_params.remote_port = port1
        net_params.local_port = port0
        obtain_result = True
        data = ["1", "2", "3"]
        print("Party 0's data:")
        print(data)
    else:
        net_params.remote_addr = host
        net_params.remote_port = port0
        net_params.local_port = port1
        data = ["2", "3", "4"]
        print("Party 1's data:")
        print(data)

    net = NetFactory.get_instance().build(NetScheme.SOCKET, net_params)
    psi = PSI(net, party, PSIScheme.ECDH_PSI)
    ret = psi.process(data, obtain_result)
    if party == 0:
        print("Result: ")
        print(ret)
