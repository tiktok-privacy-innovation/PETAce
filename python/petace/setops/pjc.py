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

from petace.setops.pysetops import pjc, PJCScheme
from petace.network import Network


class PJC:
    """
    PJC utils, now only support Circuit psi.

    Both parties input their sets and get the share of the intersection of their sets.

    Parameters
    ----------
    net : Network
        The network interface (e.g., PETAce-Network interface).
    party_id : int
        The party id of the set owner.
    pjc_scheme : PJCScheme
        Which psi scheme will use.

    Attributes
    ----------
    net : Network
        The network interface (e.g., PETAce-Network interface).
    party_id: int
        The party id of the set owner.
    pjc_scheme : PJCScheme
        Which psi scheme will use.
    """

    def __init__(self, net: "Network", party_id: int, pjc_scheme: "PJCScheme") -> None:
        self.party_id = party_id
        self.net = net
        self.pjc_scheme = pjc_scheme

    def process(self, keys: List[str], features: List[List[int]], verbose: bool = False) -> List[List[int]]:
        """
        Process psi protocol.

        Parameters
        ----------
        keys : list[str]
            The master ke.
        features : list[list[int]]
            The features corresponding to keys.
        verbose : bool
            Whether print logs.

        Returns
        -------
        list[list[int]]
            The share of features and whether they in the intersection.
        """
        return pjc(keys, features, self.party_id, verbose, self.net, self.pjc_scheme)
