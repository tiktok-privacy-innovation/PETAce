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

from typing import List

from petace.setops.pysetops import psi, PSIScheme
from petace.network import Network


class PSI:
    """
    PSI utils, now support ECDH psi and KKRT psi.

    Both parties input their sets and get the intersection of their sets.

    Parameters
    ----------
    net : Network
        The network interface (e.g., PETAce-Network interface).
    party_id :int
        The party id of the set owner.
    psi_scheme : PSIScheme
        Which psi scheme will use.

    Attributes
    ----------
    net : Network
        The network interface (e.g., PETAce-Network interface).
    party_id :int
        The party id of the set owner.
    psi_scheme : PSIScheme
        Which psi scheme will use.
    """

    def __init__(self, net: "Network", party_id: int, psi_scheme: "PSIScheme") -> None:
        self.party_id = party_id
        self.net = net
        self.psi_scheme = psi_scheme

    def process(self, input: List[str], obtain_result: bool, verbose: bool = False) -> List[str]:
        """
        Process psi protocol.

        Parameters
        ----------
        input : list[str]
            The set of each party.
        obtain_result : bool
            Whether this party get the intersection.
        verbose :bool
            Whether print logs.

        Returns
        -------
        list[str]
            The intersection if obtain_result is true, else empty list.
        """
        return psi(input, self.party_id, obtain_result, verbose, self.net, self.psi_scheme)
