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


class TestArray(SnpTestBase):

    def test_create(self, party_id):
        np.random.seed(43)
        shapes = ((), (1000,), (10000, 10))
        for shape in shapes:
            if party_id == 0:
                data = np.random.random(shape)
            else:
                data = None
            data_cipher = snp.array(data, 0)
            npt.assert_equal(data_cipher.shape, shape)
