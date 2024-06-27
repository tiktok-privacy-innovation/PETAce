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

import numpy as np
import numpy.testing as npt

import petace.securenumpy as snp
from petace.tests.utils import SnpTestBase


class TestWhere(SnpTestBase):

    def test_basic(self, party_id):
        np.random.seed(43)
        p0 = np.random.random((6, 13))
        p1 = np.random.random((6, 13))
        c0 = snp.array(p0, 0)
        c1 = snp.array(p1, 1)
        cipher_res = snp.where(c0 > c1, c0, c1)
        plain_res = np.where(p0 > p1, p0, p1)
        res = cipher_res.reveal_to(0)
        if party_id == 0:
            npt.assert_almost_equal(res, plain_res, decimal=4)
