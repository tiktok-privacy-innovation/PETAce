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


class TestNeg(SnpTestBase):

    def test_basic(self, party_id):
        arr = snp.arange(10)
        arr_neg = -arr
        res = arr_neg.reveal_to(0)
        if party_id == 0:
            npt.assert_almost_equal(res, -np.arange(10), decimal=8)


class TestInvert(SnpTestBase):

    def test_basic(self, party_id):
        arr1 = snp.array(np.array([1, 0]), 0)
        arr2 = snp.array(np.array([0, 0]), 0)
        arr = arr1 == arr2
        arr_invert = ~arr
        res = arr_invert.reveal_to(0)
        if party_id == 0:
            npt.assert_almost_equal(res, [True, False])
