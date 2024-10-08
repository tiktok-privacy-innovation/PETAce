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


class TestSum(SnpTestBase):

    def test_1d(self, party_id):
        data_cipher = snp.arange(10)
        res = snp.sum(data_cipher)
        res_plain = res.reveal_to(0)
        if party_id == 0:
            npt.assert_almost_equal(res_plain, np.sum(np.arange(10)), decimal=8)

    def test_2d(self, party_id):
        np.random.seed(43)
        data = np.random.random((10, 20))
        data_cipher = snp.array(data, 0)
        # axis = 0
        res1 = snp.sum(data_cipher, axis=0)
        res1_plain = res1.reveal_to(0)
        if party_id == 0:
            npt.assert_almost_equal(res1_plain, np.sum(data, axis=0), decimal=4)
        # axis = 1
        res2 = snp.sum(data_cipher, axis=1)
        res2_plain = res2.reveal_to(0)
        if party_id == 0:
            npt.assert_almost_equal(res2_plain, np.sum(data, axis=1), decimal=3)
        # axis = None
        res3 = snp.sum(data_cipher, axis=None)
        res3_plain = res3.reveal_to(0)
        if party_id == 0:
            npt.assert_almost_equal(res3_plain, np.sum(data, axis=None), decimal=2)
