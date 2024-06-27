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
import petace.securesql as ssql

from petace.tests.utils import SnpTestBase


class TestSecureSQL(SnpTestBase):

    def test_group_by_sum(self, party_id):
        data_a = np.array([[-15.812, -14.7387], [7.8120, -9.7387], [-2.8120, 6.7387], [1.8120, 1.7387],
                           [5.8120, 0.7387], [-7.8120, -9.7387]],
                          dtype=np.float64)
        encoding = np.array([[1, 1], [1, 1], [0, 0], [1, 1], [0, 1], [1, 1]], dtype=np.float64)
        data_b = np.array([[-14, -8.188], [-32.4774, -31.7387]], dtype=np.float64)

        input_a = snp.array(data_a, 0)
        input_coding = snp.array(encoding, 0)
        output = ssql.groupby_sum(input_a, input_coding)
        p0 = output.reveal_to(0)
        if party_id == 0:
            npt.assert_almost_equal(p0, data_b, decimal=3)

    def test_group_by_count(self, party_id):
        data_a = np.array([[-15.812, -14.7387], [7.8120, -9.7387], [-2.8120, 6.7387], [1.8120, 1.7387],
                           [5.8120, 0.7387], [-7.8120, -9.7387]],
                          dtype=np.float64)
        encoding = np.array([[1, 1], [1, 1], [0, 0], [1, 1], [0, 1], [1, 1]], dtype=np.float64)
        data_b = np.array([[4, 5], [4, 5]], dtype=np.float64)

        input_a = snp.array(data_a, 0)
        input_coding = snp.array(encoding, 0)
        output = ssql.groupby_count(input_a, input_coding)
        p0 = output.reveal_to(0)
        if party_id == 0:
            npt.assert_almost_equal(p0, data_b, decimal=3)

    def test_group_by_max(self, party_id):
        data_a = np.array([[-15.812, -14.7387], [7.8120, -9.7387], [-2.8120, 6.7387], [1.8120, 1.7387],
                           [5.8120, 0.7387], [-7.8120, -9.7387]],
                          dtype=np.float64)
        encoding = np.array([[1, 1], [1, 1], [0, 0], [1, 1], [0, 1], [1, 1]], dtype=np.float64)
        data_b = np.array([[7.8120, 7.8120], [1.7387, 1.7387]], dtype=np.float64)

        input_a = snp.array(data_a, 0)
        input_coding = snp.array(encoding, 0)
        output = ssql.groupby_max(input_a, input_coding)
        p0 = output.reveal_to(0)
        if party_id == 0:
            npt.assert_almost_equal(p0, data_b, decimal=3)

    def test_group_by_min(self, party_id):
        data_a = np.array([[-15.812, -14.7387], [7.8120, -9.7387], [-2.8120, 6.7387], [1.8120, 1.7387],
                           [5.8120, 0.7387], [-7.8120, -9.7387]],
                          dtype=np.float64)
        encoding = np.array([[1, 1], [1, 1], [0, 0], [1, 1], [0, 1], [1, 1]], dtype=np.float64)
        data_b = np.array([[-15.812, -15.812], [-14.7387, -14.7387]], dtype=np.float64)

        input_a = snp.array(data_a, 0)
        input_coding = snp.array(encoding, 0)
        output = ssql.groupby_min(input_a, input_coding)
        p0 = output.reveal_to(0)
        if party_id == 0:
            npt.assert_almost_equal(p0, data_b, decimal=3)
